from connection import get_connection

def show_tables_and_columns():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Tablas y columnas en la base de datos:")
    for table in tables:
        print(f"\nTabla: {table}")
        cursor.execute(f'PRAGMA table_info({table});')
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    conn.close()

if __name__ == "__main__":
    show_tables_and_columns()
