# /start
async def db_add_user(pool, username, telegram_id):
    async with pool.acquire() as conn:
        # Таблица пользователей
        # execute возвращает статус
        await conn.execute(
            # INSERT INTO - добавить строку
            # одна ковычка для sql, для строки кода - если умещается
            "INSERT INTO users (username, user_id) VALUES($1,$2) ON CONFLICT DO NOTHING",
            username,
            telegram_id,
        )


# Добавление заявкив таблицу ticket
async def db_add_ticket(pool, user_id, text):
    async with pool.acquire() as conn:
        # fetchrow возвращает результат строки, если есть RETURNING, в нашем случае результат id(заявки)
        row = await conn.fetchrow(
            "INSERT INTO tickets (user_id, message_text) VALUES($1,$2) RETURNING id",
            user_id,
            text,
        )
        return row[0]


# /take взять заявку
async def db_status_take(pool, worker_id, id_noti, status):
    async with pool.acquire() as conn:
        # fetchrow возвращает результат строки, если есть RETURNING, в нашем случае результат id
        result_w = await conn.execute(
            """UPDATE tickets 
                           SET status=$3, worker_id=$2 
                           WHERE id=$1
                           RETURNING worker_id""",
            id_noti,
            worker_id,
            status,
        )
        return result_w[0]


# /done Закрыть заявку
async def db_status_done(pool, worker_id, id_noti, status):
    async with pool.acquire() as conn:
        # fetchrow возвращает результат строки, если есть RETURNING, в нашем случае результат id
        await conn.execute(
            """UPDATE tickets 
                           SET status=$3, worker_id=$2 
                           WHERE id=$1""",
            id_noti,
            worker_id,
            status,
        )


# Поиск в ticket и users по username - /find @qweqwe
async def db_find_username(pool, name):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT t.id, t.message_text, t.status, t.created_at
            FROM tickets t
            JOIN users u ON u.user_id = t.user_id
            WHERE u.username = $1
                AND t.status IN ('take', 'new')
            """,
            name,
        )

    return rows


# поиск в ticket по id - /find 123
async def db_find_idnoti(pool, idnoti):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, message_text, status, created_at FROM tickets WHERE id = $1",
            idnoti,
        )
        return row


# поиск в ticket по message_text - /find qwesdf
async def db_find_az(pool, text):
    async with pool.acquire() as conn:
        row = await conn.fetch(
            """SELECT id, message_text, status, created_at 
            FROM tickets WHERE message_text ILIKE $1""",
            f"%{text}%",
        )
        return row


# re 5 послдегих сообщений из таблицы message роли - user
async def db_message_text(pool, id_noti):
    async with pool.acquire() as conn:
        row = await conn.fetch(
            """SELECT role, text FROM messages 
                WHERE ticket_id = $1
                ORDER BY created_at
                LIMIT 5""",
            id_noti,
        )
        return row


# Возвращает id заявки и стутус последней не закрытой заявки
async def db_status_noti(pool, user_id):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT id, status, worker_id, created_at
            FROM tickets
            WHERE user_id = $1
            AND status !='done'
            ORDER BY created_at DESC
            LIMIT 1""",
            user_id,
        )
        return row


# Дабоавляет текст диалога в таблицу
async def db_d_add(pool, id_noti, text, id_msg, role):
    async with pool.acquire() as conn:
        await conn.fetchrow(
            """INSERT INTO messages (ticket_id, text, id_msg, role) 
            VALUES($1,$2,$3,$4) ON CONFLICT DO NOTHING """,
            id_noti,
            text,
            int(id_msg),
            role,
        )
        return


# возвращает id сообщения и id пользователя по id заявки
async def db_re_idnoti(pool, id_msg):
    async with pool.acquire() as conn:
        ticket_id1 = await conn.fetchrow(
            "SELECT ticket_id FROM messages WHERE id_msg=$1", id_msg
        )
        user_id1 = await conn.fetchrow(
            "SELECT user_id, id FROM tickets WHERE id=$1",
            ticket_id1[0],
        )
        result = [ticket_id1[0], user_id1[0]]
        return result
