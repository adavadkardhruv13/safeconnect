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
from models.models import PetType
from qrcode import QRCode, constants
from PIL import Image
import cloudinary.uploader
from io import BytesIO
from datetime import datetime


router = APIRouter(
    prefix="/pet",
    tags=['pet']
)


def date_formate_convertion(date_of_birth_str):
    try:
        date_of_birth = datetime.strptime(date_of_birth_str, '%m/%d/%Y')
    except ValueError:
        raise ValueError("Invalid date formate")
    
    formatted_date = date_of_birth.strftime('%Y-%m-%d')
    date_of_birth = datetime.strptime(formatted_date, '%Y-%m-%d')
    
    date_value = date_of_birth.date()
    return date_value

    
    

@router.post('/post_pet_data', status_code=status.HTTP_201_CREATED)
async def post_pet_data(
    pet_name: str,
    owner_name: str,
    date_of_birth: str,
    pet_type: PetType,
    pet_gender: str,
    pet_height: str,
    pet_weight: str,
    pet_breed: str,
    some_distinctive_mark: str,
    contact_number: str,
    emergengy_number: str,
    device_image_url: UploadFile = File(),
    pool: Pool = Depends(get_pool)
):
    # Convert date_of_birth to the appropriate format
    date_of_birth = date_formate_convertion (date_of_birth)

    # Extract device image URL
    device_image_url = await upload_to_cloudinary(device_image_url)
    if not device_image_url:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload device image")

    # Prepare data tuple for SQL query
    data = (
        pet_name, owner_name, date_of_birth, pet_type, pet_gender, pet_height, pet_weight, pet_breed,
        some_distinctive_mark, contact_number, emergengy_number, device_image_url
    )

    async with pool.acquire() as connection:
        sql = '''
        INSERT INTO pet_registration_table (
            pet_name, owner_name, date_of_birth, pet_type, pet_gender, pet_height, pet_weight, pet_breed,
            some_distinctive_mark, contact_number, emergengy_number, device_image_url
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id;
        '''
        result = await connection.fetchval(sql, *data)

        # Generate QR code and upload to Cloudinary
        qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/pet/get_pet_data/{pet_name}/{owner_name}"
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
            public_id=f"{pet_name}_{owner_name}_qr_code"
        )
        qr_code_url = qr_code_upload_result["secure_url"]

        # Update database record with QR code URL
        update_query = '''
        UPDATE pet_registration_table
        SET qrcode_url = $1
        WHERE id = $2;
        '''
        await connection.execute(update_query, qr_code_url, result)

        # Return success response with inserted device ID and URLs
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Device registered successfully",
                "data": {
                    "device_id": result,
                    "qrcode_url": qr_code_url,
                    "device_image_url": device_image_url  # Return the original UploadFile object URL
                }
            }
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
        
        

@router.get("/get_pet_data", status_code=status.HTTP_200_OK)
async def get_pet_data(pool:Pool = Depends(get_pool)) :
    data = await Modelquery(pool).get_pet_data()
    return{'message':'Success', 'Data':data}


@router.get("/get_pet_data_by_pet_name/{pet_name}/{owner_name}", status_code=status.HTTP_200_OK)
async def get_pet_data(pet_name:str, owner_name, pool:Pool = Depends(get_pool)) :
    data = await Modelquery(pool).get_pet_data_by_pet_name(pet_name, owner_name)
    return{'message':'Success', 'Data':data}