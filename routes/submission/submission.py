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
from qrcode import QRCode, constants
from PIL import Image
import cloudinary.uploader
from io import BytesIO



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
                                                   public_id=f"{vehicle_no}_qr_code")
            
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
                content={"message": "Success", "data": {"vehicle_id": result, "qrcode_url": qr_code_url}}
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

@router.put('/update_vehicle_data/{vehicle_no}', status_code=status.HTTP_200_OK)
async def update_vehicle_registration_data(
    owner_name: str,
    vehicle_type: VehicleType,
    vehicle_brand: VehicleBrand,
    vehicle_no: str,
    email: str,
    contact_number: str,
    emergency_number: str,
    #qrcode_url:str,
    pool: Pool = Depends(get_pool)
):
    data = (owner_name, vehicle_type, vehicle_brand, vehicle_no, email, contact_number, emergency_number)
    
    async with pool.acquire() as connection:
        existing_record = await Modelquery(pool).get_vehicle_registration_data_by_vehicle_no(vehicle_no)
        if not existing_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with ID {vehicle_no} not found")
        
        sql = '''
                UPDATE vehicle_registration_data
            SET
                owner_name = $1,
                vehicle_type = $2,
                vehicle_brand = $3,
                email = $5,
                contact_number = $6,
                emergency_number = $7
            WHERE vehicle_no = $4;
                '''
                
        await connection.execute(sql,*data)
        updated_record = await Modelquery(pool).get_vehicle_registration_data_by_vehicle_no(vehicle_no)
        qrcode_url = updated_record[0]['qrcode_url']
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Vehicle data updated successfully"})