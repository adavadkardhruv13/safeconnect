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
                query = 'SELECT * FROM vehicle_registration_data WHERE contact_number = {contact_number};'
                rows = await connection.fetch(query, contact_number)
                data = [dict(row) for row in rows]
        return data
