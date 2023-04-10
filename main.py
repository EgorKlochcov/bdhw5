import psycopg2

def create_db(conn):
    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS clients
    ( id serial PRIMARY KEY,
    first_name varchar(40) NOT NULL,
    last_name varchar(40) NOT NULL, 
    email varchar(80) UNIQUE);
    """)
    conn.commit()

    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS phones
    ( id serial PRIMARY KEY,
    phone_num BIGINT UNIQUE,
    client_id INTEGER NOT NULL REFERENCES clients(id));
    """)
    conn.commit()


def add_phone(conn, phone_num, client_id):
    conn.cursor().execute("""
    INSERT INTO phones
    (phone_num, client_id) VALUES(%s, %s);""", (phone_num, client_id))
    conn.commit()


def add_client(conn, id, first_name, last_name, email, phone=None):
    conn.cursor().execute("""
    INSERT INTO clients 
    (id, first_name, last_name, email) 
    VALUES(%s,%s, %s, %s);""", (id, first_name, last_name, email))
    conn.commit()

    if phone:
        add_phone(conn, phone, id)


def delete_phone(conn, phone_num):
    conn.cursor().execute("""DELETE FROM phones WHERE phone_num = %s ;""", (phone_num,))
    conn.commit()


def delete_client(conn, id):
    conn.cursor().execute("""DELETE FROM phones WHERE client_id = %s;""", (id,))
    conn.cursor().execute("""DELETE FROM clients WHERE id = %s;""", (id,))
    conn.commit()



def change_client(conn, client_id, new_phone=None, old_phone=None, **change_params):
    if new_phone and old_phone:
        conn.cursor().execute("""
        UPDATE phones
        SET phone_num=%s 
        WHERE phone_num = %s AND client_id=%s ;""",(new_phone, old_phone, client_id))
        conn.commit()

    params = ", ".join(list(map(lambda x: x + '=%s', change_params.keys())))
    value = tuple(change_params.values()) + tuple(str(client_id))
    query = f""" UPDATE clients SET {params} WHERE id=%s;"""
    conn.cursor().execute(query, value)
    conn.commit()


def search_client(conn,**search_data):
    params = ", ".join(list(map(lambda x: x + '=%s', search_data.keys())))
    value = tuple(search_data.values())
    query = f"""
    SELECT *, phones.client_id FROM clients 
    JOIN phones ON phones.client_id = clients.id
    WHERE {params};"""
    with conn.cursor() as cur:
        cur.execute(query, value)
        print(cur.fetchall())



conn = psycopg2.connect(database='SOME_DB', user='postgres', password="SOME_PASSWORD")
with conn:
<<<<<<< HEAD


=======
    create_db(conn)
    add_client(conn, 1, 'Ivan', 'Ivanov', 'iviv123@mail.ru', 88005553535)
    add_phone(conn, 89826661144, 1)
    delete_phone(conn, 89826661144)
    change_client(conn, 1, first_name='Ivan')
    search_client(conn, email='iviv123@mail.ru')
    delete_client(conn, 1)
>>>>>>> 76e49e4 (upd)
conn.close()