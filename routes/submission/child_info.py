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
from urllib.parse import quote

router = APIRouter(
    prefix="/child",
    tags=['child']
)


#def date_formate_convertion(date_of_birth_str):
    #try:
        #date_of_birth = datetime.strptime(date_of_birth_str, '%d/%m/%Y')
    #except ValueError:
    #    raise ValueError("Invalid date formate")
    
    #formatted_date = date_of_birth.strftime('%Y-%m-%d')
    #date_of_birth = datetime.strptime(formatted_date, '%Y-%m-%d')
    
    #date_value = date_of_birth.date()
    #return date_value


@router.get('/get_child_data', status_code=status.HTTP_200_OK)
async def get_child_data(pool:Pool = Depends(get_pool)):
    data = await Modelquery(pool).get_child_data()
    return{'message':'success', 'Data':data}

@router.post('/post_child_data', status_code=status.HTTP_201_CREATED)
async def post_child_data(
    child_data: ChildRegistration,
    pool:Pool = Depends(get_pool)
):
    data = child_data.dict()
    child_name = data['child_name']
    date_of_birth = data['date_of_birth']
    father_name = data['father_name']
    mother_name = data['mother_name']
    email = data['email']
    contact_number = data['contact_number']
    emergency_number = data['emergency_number']
    #date_of_birth = date_formate_convertion(date_of_birth)
    
    data=(
        child_name, str(date_of_birth) , father_name, mother_name, email, 
        contact_number, emergency_number
    )
    
    async with pool.acquire() as connection:
        
        sql = '''
        INSERT INTO child_registration_table(
            child_name, date_of_birth, father_name, mother_name, email, 
            contact_number, emergency_number
        )
        VALUES($1,$2,$3,$4,$5,$6,$7)
        RETURNING id;
        '''
        
        
        result = await connection.fetchval(sql, *data)
        
        #encoding names to make it compatible for url
        encoded_child_name = quote(child_name)
        encoded_father_name = quote(father_name)
        
        qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/child/get_child_data/{encoded_child_name}/{encoded_father_name}"
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
            public_id=f"{child_name}_{father_name}_qr_code"
        )
        qr_code_url = qr_code_upload_result["secure_url"]

        # Update database record with QR code URL
        update_query = '''
        UPDATE child_registration_table
        SET qrcode_url = $1
        WHERE id = $2;
        '''
        await connection.execute(update_query, qr_code_url, result)

        # Return success response with inserted device ID and URLs
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Child registered successfully",
                "data": {
                    "device_id": result,
                    "qrcode_url": qr_code_url,
                    }
            }
        )


@router.get('/get_child_data/{child_name}/{father_name}', status_code=status.HTTP_200_OK)
async def get_child_data(child_name:str, father_name:str, pool:Pool=Depends(get_pool)):
    
    data = await Modelquery(pool).get_child_data_by_name(child_name, father_name)
    #return{"message":"Success","Data":data}
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No data found for child_name: {child_name} and father name {father_name}")
    
    return {"message": "Success", "Data": data}