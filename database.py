import psycopg2 

def database_connection(): 
    try:  
        connection = psycopg2.connect(database="gia", user="postgres", password="", host="localhost", port="5432")  
        print("Подключение успешно установлено!")  
        return connection
    except Exception as e:  
        print(f"Ошибка подключения: {e}")  

def get_data(table_name: str, connection):
    if not table_name.replace('_', '').isalnum():
        raise ValueError("Недопустимое имя таблицы")
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return columns, rows
    