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
from models.models import VehicleType, VehicleBrand
from qrcode import make as make_qr_code
from PIL import Image
import cloudinary.uploader



router = APIRouter(
    prefix="/vehicle",
    tags=['Submission']
)


@router.get('/get_vehicle_data', status_code=status.HTTP_201_CREATED)
async def get_vehicle_data(pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_vehicle_registration_data()
    return{"message":"Success","Data":data}


@router.post('/post_vehicle_data', status_code=status.HTTP_201_CREATED)
async def post_vehicle_data(
    owner_name: str,
    vehicle_type: VehicleType,
    vehicle_brand: VehicleBrand,
    vehicle_no: str,
    email: str,
    contact_number: str,
    emergency_number: str,
    pool: Pool = Depends(get_pool)
):
    # Prepare data for insertion
    data = (owner_name, vehicle_type, vehicle_brand, vehicle_no, email, contact_number, emergency_number)
    
    async with pool.acquire() as connection:
        
            # Define the SQL query with placeholders and RETURNING clause
            query = """
                INSERT INTO vehicle_registration_data (
                    owner_name, vehicle_type, vehicle_brand,
                    vehicle_no, email, contact_number, emergency_number
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id;
            """
            # Execute the SQL query with data values and fetch the result
            result = await connection.fetchval(query, *data)
            
            #generate QRCODE
            qr_data = f"https://safeconnect-e81248c2d86f.herokuapp.com/vehicle/get_vehicle_data/{vehicle_no}"
            qr_code = make_qr_code(qr_data)
            qr_code_image = qr_code.get_image()
            #qr_code_image.save(f"qr_codes/{vehicle_no}.png")
            
            # Upload QR code image to Cloudinary
            upload_result = cloudinary.uploader.upload(qr_code_image, 
                                                   folder="qr_codes", 
                                                   public_id=vehicle_no)
            
            qr_code_url = upload_result["secure_url"]
            
            await connection.execute(
            """
            UPDATE vehicle_registration_data
            SET qrcode_url = $1
            WHERE id = $2;
            """,
            qr_code_url,
            result,
        )
            
            # Construct response with inserted vehicle_id
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Success", "data": {"vehicle_id": result}}
            )
        #except Exception as e:
            # Handle any database-related exceptions
            #raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        

@router.get('/get_vehicle_data/{vehicle_no}', status_code=status.HTTP_201_CREATED)
async def get_vehicle_registration_data_by_vehicle_no(vehicle_no:str, pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_vehicle_registration_data_by_vehicle_no(vehicle_no)
    return{"message":"Success","Data":data}


@router.get('/get_vehicle_data/{contact_number}', status_code=status.HTTP_201_CREATED)
async def get_vehicle_registration_data_by_contact_number(contact_number:int ,pool:Pool = Depends(get_pool)):
    
    data = await Modelquery(pool).get_vehicle_registration_data_by_contact_number(contact_number)
    return{"message":"Success","Data":data}