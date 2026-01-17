from database import engine

def test_connection():
    try:
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    test_connection()
