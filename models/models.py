from pydantic import BaseModel
from enum import Enum

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
    

class VehicleRegistration(BaseModel):
    owner_name : str
    vehicle_type : VehicleType
    vehicle_brand : str
    vehicle_no : str
    email : str
    contact_number : str
    emergency_number : str