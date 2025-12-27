from dotenv import load_dotenv
import os
import asyncpg

load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")


# создание пулла соединений, возвращает пулл соединений
async def create_pool():
    return await asyncpg.create_pool(
        user=USER, password=PASSWORD, database=DATABASE, host=HOST
    )


# Только для start, чисто для инфы какие пользователи, нечего не меняем
async def setup_table(pool):
    async with pool.acquire() as conn:
        # Таблица пользователей
        await conn.execute(
            """ CREATE TABLE IF NOT EXISTS users(
                           id SERIAL PRIMARY KEY,
                           user_id BIGINT UNIQUE,
                           username TEXT,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
                           """
        )
        print("Проверка таблицы [users]: True")

        # Таблица тикетов
        await conn.execute(
            """ CREATE TABLE IF NOT EXISTS tickets(                            
                        id SERIAL PRIMARY KEY, 
                        user_id BIGINT REFERENCES users(user_id),
                        message_text TEXT,
                        status TEXT DEFAULT 'new',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); """
        )
        print("Проверка таблицы [tickets]: True")

        # Таблица диалога
        await conn.execute(
            """ CREATE TABLE IF NOT EXISTS messages(                            
                        id SERIAL PRIMARY KEY, 
                        ticket_id INTEGER NOT NULL,
                        role TEXT NOT NULL, 
                        text TEXT NOT NULL,
                        id_msg INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        
                        
                        CONSTRAINT fk_ticket
                            FOREIGN KEY (ticket_id)
                            REFERENCES tickets (id)
                            ON DELETE CASCADE);"""
        )
        print("Проверка таблицы [messages]: True")
