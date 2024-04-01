from contextlib import contextmanager
import psycopg2.pool


class Database:
    def __init__(self):
        self.db = None
        self.cursor = None

    def create_tables(self):
        # Create tables if it doesn't exist
        conn = psycopg2.connect(
            user="admin",
            password="S3cret",
            host="postgres",
            port="5432",
            database="kanastra",
        )
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS billings_uploads (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        createdAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updatedAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        status VARCHAR(100) NOT NULL DEFAULT 'ACKNOWLEDGED'
                    )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS billings (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255),
                            governmentId INTEGER,
                            email VARCHAR(255),
                            debtAmount FLOAT,
                            debtDueDate DATE,
                            debtId UUID,
                            createdAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            updatedAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                            status VARCHAR(100) NOT NULL DEFAULT 'ACKNOWLEDGED',
                            isDeleted BOOLEAN NOT NULL DEFAULT false,
                            uploadId INTEGER,
                            CONSTRAINT fk_billings_uploads
                                FOREIGN KEY(uploadId) 
                                    REFERENCES billings_uploads(id)
                        )"""
        )

        conn.commit()
        conn.close()

    def connect(self):
        conn = psycopg2.pool.SimpleConnectionPool(
            2,
            5,
            user="admin",
            password="S3cret",
            host="postgres",
            port="5432",
            database="kanastra",
        )

        self.db = conn
        self.cursor = conn.getconn().cursor()

    @contextmanager
    def get_connection(self):
        con = self.db.getconn()
        try:
            yield con
        finally:
            self.db.putconn(con)

    def disconnect(self):
        self.db.closeall()


instance = Database()
