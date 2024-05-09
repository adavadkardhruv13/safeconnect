from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import date

class VehicleType(str, Enum):
    Car = 'Car'
    ElectricCar = 'Electric Car'
    Truck = 'Truck'
    Van = 'Van'
    Motorcycle = 'Motorcycle'
    ElectricMotorcycle = 'eMotorcycle'
    Scooty = 'Scooty'
    ElectricScooty = 'Electric Scooty'
    HybridCar = 'Hybrid Car'
    
    
class VehicleBrand(str, Enum):
    Hero_MotoCorp = 'Hero MotoCorp'
    Bajaj_Auto = 'Bajaj Auto'
    TVS_Motor_Company = 'TVS Motor Company'
    Honda_Motorcycle_Scooter_India = 'Honda Motorcycle & Scooter India (HMSI)'
    Yamaha_Motor_India = 'Yamaha Motor India'
    Suzuki_Motorcycle_India = 'Suzuki Motorcycle India Private Limited'
    Royal_Enfield = 'Royal Enfield'
    KTM_India = 'KTM India'
    Mahindra_Two_Wheelers = 'Mahindra Two Wheelers'
    Vespa_Piaggio_India = 'Vespa (Piaggio India)'
    Aprilia_Piaggio_India = 'Aprilia (Piaggio India)'
    BMW_Motorrad = 'BMW Motorrad'
    Harley_Davidson_India = 'Harley-Davidson India'
    Revolt_Motors = 'Revolt Motors'
    Java = 'Java'
    Maruti_Suzuki = 'Maruti Suzuki'
    Hyundai = 'Hyundai'
    Tata_Motors = 'Tata Motors'
    Mahindra_Mahindra = 'Mahindra & Mahindra'
    Kia_Motors_India = 'Kia Motors India'
    Toyota_Kirloskar_Motor = 'Toyota Kirloskar Motor'
    Honda_Cars_India = 'Honda Cars India'
    Volkswagen_India = 'Volkswagen India'
    Skoda_Auto_India = 'Skoda Auto India'
    Ford_India = 'Ford India'
    MG_Motor_India = 'MG Motor India'
    Renault_India = 'Renault India'
    Nissan_India = 'Nissan India'
    Jeep_FCA_India_Automobiles = 'Jeep (FCA India Automobiles)'
    BMW_India = 'BMW India'
    Mercedes_Benz_India = 'Mercedes-Benz India'
    Audi_India = 'Audi India'
    Volvo_Cars_India = 'Volvo Cars India'
    

class DeviceType(str, Enum):
    Cell_Phone = 'Cell Phone',
    HeadPhone =  'HeadPhone',
    EarPhone = "EarPhone",
    DigitalWatch = 'Digital Watch',
    Speaker = 'Speaker',
    Laptop = 'Laptop',
    
class PetType(str, Enum):
    Dog = "Dog",
    Cat = "Cat",
    Cow = "Cow",
    Goat = "Goat"
    

class VehicleRegistration(BaseModel):
    owner_name : str
    vehicle_type : VehicleType
    vehicle_brand : str
    vehicle_no : str
    email : str
    contact_number : str
    emergency_number : str
    
    
    
class DeviceRegistration(BaseModel):
    owner_name : str
    device_type : DeviceType
    device_name : str
    email : str
    contact_number : str
    emergency_number : str
    qrcode_url : str
    
class PetRegistration(BaseModel):
    pet_name : str
    owner_name : str
    date_of_birth : date
    pet_type : PetType
    pet_gender : str
    pet_height : str
    pet_weight : str
    pet_breed : str
    some_distinctive_mark : str
    contact_number : str
    emergengy_number : str
    qrcode_url: Optional[str] = None
    device_image_url: Optional[str] = None
    
class ChildRegistration(BaseModel):
    child_name : str
    date_of_birth : str
    father_name : str
    mother_name : str
    email : str
    contact_number : str
    emergency_number : str
    qrcode_url  : str


class MedicalRegistration(BaseModel):
    name:str
    phone_number:str
    email:str
    blood_group: str
    blood_pressure: str
    blood_pressure_patient:bool
    sugar_patient:bool
    allergies: str
    medications: str
    organ_donor: Optional[bool] = None
    medical_note: Optional[str] = None
    disease: Optional[str] = None
    immunization: Optional[str] = None
    qrcode_url:Optional[str] = None