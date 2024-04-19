from fastapi import FastAPI, status, HTTPException, UploadFile, File
from fastapi import APIRouter, Depends
from models.models import *
from models.db_utils import * 
import json
from asyncpg.pool import Pool
from queryhelper.modelquery import Modelquery
from dotenv import dotenv_values
from models.db_utils import *
from fastapi.responses import JSONResponse
from models.models import DeviceType
from qrcode import QRCode, constants
from PIL import Image
import cloudinary.uploader
from io import BytesIO


router = APIRouter(
    prefix="/device",
    tags=['device']
)


@router.get("/get_device_record", status_code=status.HTTP_200_OK)
async def get_device_record(pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_device_registration_data()
    return{"message":"Success","Data":data}


@router.post("/post_device_record", status_code=status.HTTP_201_CREATED)
async def post_device_record(
    owner_name: str,
    device_type: DeviceType,  # Assuming DeviceType is a string type
    device_name: str,
    email: str,
    contact_number: str,
    emergency_number: str,
    device_image: UploadFile = File(),
    pool: Pool = Depends(get_pool)
):
    data = (owner_name, device_type, device_name, email, contact_number, emergency_number)

    async with pool.acquire() as connection:
        # Insert device registration data and retrieve the inserted ID
        insert_query = '''
        INSERT INTO device_record_data (
            owner_name, device_type, device_name,
            email, contact_number, emergency_number
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
        '''
        result = await connection.fetchval(insert_query, *data)

        # Upload device image to Cloudinary
        device_image_url = await upload_to_cloudinary(device_image)
        if not device_image_url:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload device image")

        # Generate QR code and upload to Cloudinary
        qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/device/get_device_record/{owner_name}/{contact_number}"
        qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_code_image = qr.make_image(fill_color="black", back_color="white")

        qr_code_stream = BytesIO()
        qr_code_image.save(qr_code_stream, format="PNG")
        qr_code_stream.seek(0)

        qr_code_upload_result = cloudinary.uploader.upload(
            qr_code_stream,
            folder="qr_codes",
            public_id=f"{owner_name}_qr_code"
        )
        qr_code_url = qr_code_upload_result["secure_url"]

        # Update database record with QR code URL and device image URL
        update_query = '''
        UPDATE device_record_data
        SET qrcode_url = $1, device_image_url = $2
        WHERE id = $3;
        '''
        await connection.execute(update_query, qr_code_url, device_image_url, result)

        # Return success response with inserted device ID and URLs
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Device registered successfully",
                    "data": {"device_id": result, "qrcode_url": qr_code_url, "device_image_url": device_image_url}}
        )
        
        
async def upload_to_cloudinary(file: UploadFile):
    try:
        # Read file contents into memory
        contents = await file.read()

        # Upload file to Cloudinary and retrieve secure URL
        upload_result = cloudinary.uploader.upload(contents, folder="device_images")

        return upload_result["secure_url"]
    except Exception as e:
        print(f"Error uploading file to Cloudinary: {e}")
        return None
    
    
@router.get("/get_device_record/{owner_name}/{contact_number}", status_code=status.HTTP_200_OK)
async def get_device_record(owner_name : str, contact_number : str, pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_device_registration_data_by_owner_name(owner_name, contact_number)
    #return{"message":"Success","Data":data}
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for owner_name: {owner_name} and contact number {contact_number}")
    
    return {"message": "Success", "Data": data}

@router.put("/update_device_record/{owner_name}/{contact_number}", status_code=status.HTTP_200_OK)
async def update_device_record(
    owner_name: str,
    contact_number: str,
    device_type: str,  # Assuming DeviceType is a string type
    device_name: str,
    email: str,
    emergency_number: str,
    device_image: UploadFile = File(None),
    pool: Pool = Depends(get_pool)
):
    try:
        # Acquire a connection from the pool
        async with pool.acquire() as connection:
            # Begin a transaction to perform multiple operations atomically
            async with connection.transaction():
                # Check if the device record exists
                existing_record = await Modelquery(pool).get_device_registration_data_by_owner_name(owner_name, contact_number)
                if not existing_record:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device record not found")

                # Update device record in the database
                update_query = '''
                UPDATE device_record_data
                SET
                    device_type = $1,
                    device_name = $2,
                    email = $3,
                    emergency_number = $4
                WHERE
                    owner_name = $5 AND contact_number = $6;
                '''
                await connection.execute(update_query, device_type, device_name, email, emergency_number, owner_name, contact_number)

                # Upload device image to Cloudinary (if provided)
                if device_image:
                    device_image_url = await upload_to_cloudinary(device_image)
                    if not device_image_url:
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload device image")

                    # Update device image URL in the database
                    await connection.execute(
                        '''
                        UPDATE device_record_data
                        SET device_image_url = $1
                        WHERE owner_name = $2 AND contact_number = $3;
                        ''',
                        device_image_url,
                        owner_name,
                        contact_number
                    )

                # Retrieve updated record to get the new QR code URL
                updated_record = await Modelquery(pool).get_device_registration_data_by_owner_name(owner_name, contact_number)
                qrcode_url = updated_record[0]['qrcode_url']

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"message": "Device data updated successfully", "qrcode_url": qrcode_url}
                )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update device: {str(e)}")
