import psycopg2


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def create_tables(self):
        # Create tables if it doesn't exist

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS billings_uploads (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        createdAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        updatedAt TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                        status VARCHAR(100) NOT NULL DEFAULT 'ACKNOWLEDGED'
                    )"""
        )

        self.cursor.execute(
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

    def connect(self):
        conn = psycopg2.connect("dbname=kanastra user=gustavo")

        self.connection = conn
        self.cursor = conn.cursor()

    def disconnect(self):
        self.connection.close()

    def toJSON(self, rows, one=False):
        r = [
            dict((self.cursor.description[i][0], value) for i, value in enumerate(row))
            for row in rows
        ]
        return (r[0] if r else None) if one else r


instance = Database()
