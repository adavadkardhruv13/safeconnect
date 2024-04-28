import asyncpg
from asyncpg.pool import Pool
from fastapi import Depends
from dotenv import dotenv_values

config = dotenv_values(".env")


async def get_pool()->Pool:
    return await asyncpg.create_pool(
        user = config['DB_USER'],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        
    )
    
    
class CreateVehicleRegisterationTable:
    def __init__(self, pool: Pool):
        self.pool = pool
            # Call the asynchronous method to create the users table
            
    async def create_vehicle_registration_table(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''
                    CREATE TABLE IF NOT EXISTS vehicle_registration_data (
                        id SERIAL PRIMARY KEY,
                        owner_name VARCHAR(255),
                        vehicle_type VARCHAR(255),
                        vehicle_brand VARCHAR(255),
                        vehicle_no VARCHAR(255),
                        email VARCHAR(255),
                        contact_number VARCHAR(255) UNIQUE,
                        emergency_number VARCHAR(255)
                    )
                '''
        
                # Execute the SQL query to create the table
                await connection.execute(query)
    
    
    
class CreateDeviceRegisterationTable:
    def __init__(self, pool: Pool):
        self.pool = pool
        
    async def create_device_record_table(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''
                    CREATE TABLE IF NOT EXISTS device_record_data(
                        id SERIAL PRIMARY KEY,
                        owner_name VARCHAR(255),
                        device_type VARCHAR(255),
                        device_name VARCHAR(255),
                        email VARCHAR(255),
                        contact_number VARCHAR(255),
                        emergency_number VARCHAR(255),
                        qrcode_url VARCHAR(255),
                        device_image_url VARCHAR(255)
                        
                    )'''
                    
                await connection.execute(query)
                
                
class CreatePetregistrationTable:
    def __init__(self, pool: Pool):
        self.pool = pool
        
        
    async def create_pet_table(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''
                CREATE TABLE IF NOT EXISTS pet_registration_table(
                    id SERIAL PRIMARY KEY,
                    pet_name VARCHAR(255),
                    owner_name VARCHAR(255),
                    date_of_birth DATE,
                    pet_type VARCHAR(255),
                    pet_gender VARCHAR(255),
                    pet_height VARCHAR(255),
                    pet_weight VARCHAR(255),
                    pet_breed VARCHAR(255),
                    some_distinctive_mark VARCHAR(255),
                    contact_number VARCHAR(255),
                    emergengy_number VARCHAR(255),
                    qrcode_url VARCHAR(255),
                    device_image_url VARCHAR(255)
                )
                '''
                await connection.execute(query)


class CreateChildregistrationTable:
    def __init__(self, pool: Pool):
        self.pool = pool
                
    async def create_child_table(self):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                
                query = '''
                    CREATE TABLE IF NOT EXISTS child_registration_table(
                        id SERIAL PRIMARY KEY,
                        child_name VARCHAR(255),
                        date_of_birth VARCHAR(255),
                        father_name VARCHAR(255),
                        mother_name VARCHAR(255),
                        email VARCHAR(255),
                        contact_number VARCHAR(255),
                        emergency_number VARCHAR(255),
                        qrcode_url VARCHAR(255)
                    )'''
                    
                await connection.execute(query)