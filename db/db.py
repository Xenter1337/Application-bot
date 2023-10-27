import asyncpg
from db.config import HOST, USER, PASSWORD, DATABASE


class DataBase:

    async def start_db(self):
        self.conn = await asyncpg.connect(host=HOST, user=USER, database=DATABASE, password=PASSWORD)
        await self.conn.execute("""CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            chat_id INTEGER,
            first TEXT,
            second TEXT,
            third TEXT,
            four TEXT,
            status TEXT)""")
    
    async def add_user(self, data):
        await self.conn.execute(f"""INSERT INTO users(username, chat_id, first, second, third, four, status) VALUES(
            '{data['username']}',
            '{data['chat_id']}',
            '{data['first']}',
            '{data['second']}',
            '{data['third']}',
            '{data['four']}',
            'process')""")
        
    async def select_by_id(self, id):
       result = await self.conn.fetchval(f"SELECT username FROM users WHERE chat_id = '{id}'")
       return result
   
    async def select_app(self):
        try:
            res = dict(await self.conn.fetchrow("SELECT * FROM users WHERE status = 'process'"))
        except TypeError:
            return None
        
        return res
    
    async def update_status(self, chat_id, status):
        await self.conn.execute(f"UPDATE users SET status = '{status}' WHERE chat_id = {chat_id}")
    
       
        
    async def on_shut(self):
        self.conn.close()