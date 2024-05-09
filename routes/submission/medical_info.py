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
    prefix="/medical",
    tags=['medical'] 
)


@router.post('/post_medical_data', status_code=status.HTTP_201_CREATED)
async def post_medical_data(medical_data: MedicalRegistration, pool:Pool = Depends(get_pool)):
    
    
    data = medical_data.dict()
    name = data['name']
    phone_number = data['phone_number']
    email = data['email']
    blood_group = data['blood_group']
    blood_pressure = data['blood_pressure']
    blood_pressure_patient = 'true' if data['blood_pressure_patient'] else 'false'
    sugar_patient = 'true' if data['sugar_patient'] else 'false'
    allergies = data['allergies']
    medications = data['medications']
    organ_donor = 'true' if data['organ_donor'] else 'false'
    medical_note = data['medical_note']
    disease = data['disease']
    immunization = data['immunization']
    qrcode_url = data['qrcode_url']
    
    async with pool.acquire() as connection:
        
        query = """
        INSERT INTO medical_registration_data(
            name, phone_number, email, blood_group, blood_pressure,
            blood_pressure_patient,sugar_patient, allergies, medications,
            organ_donor, medical_note, disease, immunization, qrcode_url
            ) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
            RETURNING id;
            """
        
        result = await connection.fetchval(query, name, phone_number, email, blood_group, blood_pressure, 
                                        blood_pressure_patient,sugar_patient, allergies, medications,
                                        organ_donor, medical_note, disease, immunization,qrcode_url)
        
         #generate QRCODE
        qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/medical/get/medical_record/{name}"
        qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_code_image = qr.make_image(fill_color="black", back_color="white")
        #qr_code_image.save(f"qr_codes/{vehicle_no}.png")
            
        qr_code_stream = BytesIO()
        qr_code_image.save(qr_code_stream, format="PNG")  # Save the image to the byte stream
        qr_code_stream.seek(0)
            
            # Upload QR code image to Cloudinary
        upload_result = cloudinary.uploader.upload(qr_code_stream, 
                                                   folder="qr_codes", 
                                                   public_id=f"{name}_qr_code")
            
        qr_code_url = upload_result["secure_url"]
            
        await connection.execute(
            """
        UPDATE medical_registration_data
        SET qrcode_url = $1 
        WHERE id = $2;
        """,
        qr_code_url,
        result,
    )
            
        # Construct response with inserted vehicle_id
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Success", "data": {"medical_id": result, "qrcode_url": qr_code_url}}
        )
        
@router.get('/get_medical_data/', status_code=status.HTTP_201_CREATED)
async def get_medical_data( pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_medical_data()
    return{"message":"Success","Data":data}


@router.get('/get_medical_data/{name}/{phone_number}', status_code=status.HTTP_201_CREATED)
async def get_medical_data_by_name(name:str, phone_number:str, pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_medical_data_by_name(name, phone_number)
    return{"message":"Success","Data":data}