from fastapi import FastAPI, status, HTTPException
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
    owner_name : str,
    device_type : DeviceType,
    device_name : str,
    email : str,
    contact_number : str,
    emergency_number : str,
    
    pool: Pool = Depends(get_pool)
):

    data = (owner_name, device_type, device_name, email, contact_number, emergency_number ) 
    
    async with pool.acquire() as connection:
        
        query = '''
        INSERT INTO device_record_data(
            owner_name, device_type, device_name, 
            email, contact_number, emergency_number)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
            
        '''
        
        result = await connection.fetchval(query, *data)

        qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/device/get_device_record/{owner_name}"
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

        upload_result = cloudinary.uploader.upload(qr_code_stream, 
                                                   folder="qr_codes", 
                                                   public_id = f"{owner_name}_qr_code")

        qr_code_url = upload_result["secure_url"]

        await connection.execute(
            """
            UPDATE device_record_data
            SET qrcode_url = $1
            WHERE id = $2;
            """,
            qr_code_url,
            result,
        )
            
            # Construct response with inserted vehicle_id
        return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Success", "data": {"device_id": result, "qrcode_url": qr_code_url}}
            )
    
    
@router.get("/get_device_record/{owner_name}", status_code=status.HTTP_200_OK)
async def get_device_record(owner_name : str, pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_device_registration_data_by_owner_name(owner_name)
    #return{"message":"Success","Data":data}
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for owner_name: {owner_name}")
    
    return {"message": "Success", "Data": data}