class Modelquery:
    def __init__(self, conn) -> None:
        self.conn = conn

    async def get_vehicle_registration_data(self):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM vehicle_registration_data;'
                rows = await connection.fetch(query)
                data = [dict(row) for row in rows]
        return data
    
    
    async def get_vehicle_registration_data_by_vehicle_no(self, vehicle_no):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM vehicle_registration_data WHERE vehicle_no = $1;'
                rows = await connection.fetch(query, vehicle_no)
                data = [dict(row) for row in rows]
        return data
    
    async def get_vehicle_registration_data_by_contact_number(self, contact_number):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM vehicle_registration_data WHERE contact_number = $1;'
                rows = await connection.fetch(query, contact_number)
                data = [dict(row) for row in rows]
        return data
    
    
    async def update_vehicle_registration_data(self, vehicle_no):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM vehicle_registration_data WHERE vehicle_no = $1;'
                rows = await connection.fetch(query, vehicle_no)
                data = [dict(row) for row in rows]
        return data
    
    async def get_device_registration_data(self):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM device_record_data;'
                rows = await connection.fetch(query)
                data = [dict(row) for row in rows]
        return data
    
    
    async def get_device_registration_data_by_owner_name(self, owner_name, contact_number):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM device_record_data WHERE owner_name = $1 AND contact_number = $2;'
                rows = await connection.fetch(query, owner_name, contact_number)
                data = [dict(row) for row in rows]
        return data
    
    async def get_pet_data(self):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM pet_registration_table ;'
                rows = await connection.fetch(query)
                data = [dict(row) for row in rows]
        return data
    
    
    async def get_pet_data_by_pet_name(self, pet_name, contact_number):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM pet_registration_table WHERE pet_name = $1 AND contact_number = $2;'
                rows = await connection.fetch(query, pet_name, contact_number)
                data = [dict(row) for row in rows]
        return data
    
    async def get_child_data(self):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM child_registration_table ;'
                rows = await connection.fetch(query)
                data = [dict(row) for row in rows]
        return data
    
    async def get_child_data_by_name(self, child_name, father_name):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM child_registration_table WHERE child_name = $1 AND father_name=$2;'
                rows = await connection.fetch(query, child_name, father_name )
                data = [dict(row) for row in rows]
        return data
    
    
    async def get_medical_data(self):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM medical_registration_data ;'
                rows = await connection.fetch(query )
                data = [dict(row) for row in rows]
        return data
    
    
    async def get_medical_data_by_name(self, name, phone_number):
        async with self.conn.acquire() as connection:
            async with connection.transaction():
                query = 'SELECT * FROM medical_registration_data WHERE name = $1 AND phone_number=$2 ;'
                rows = await connection.fetch(query, name, phone_number)
                data = [dict(row) for row in rows]
        return data
    
                
                

