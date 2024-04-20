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
from datetime import datetime


router = APIRouter(
    prefix="/device",
    tags=['device']
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

