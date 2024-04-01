from datetime import datetime
from typing import List
from fastapi import HTTPException
from dependencies import database
from psycopg2.extras import execute_batch, RealDictCursor


def save_single_billing(csv_row, uploadId):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO billings (
                        name,
                        governmentId,
                        email,
                        debtAmount,
                        debtDueDate,
                        debtId,
                        uploadId
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                [*csv_row, uploadId],
            )
            conn.commit()
        except Exception as error:
            conn.rollback()
            debdtId = csv_row[5]
            print("save_single_billing error", error)
            raise HTTPException(
                status_code=500, detail=f"Failed to save billing. debtId = {debdtId}"
            )


def insert_csv_to_database(csv):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            stmt = """INSERT INTO billings (
                        name,
                        governmentId,
                        email,
                        debtAmount,
                        debtDueDate,
                        debtId,
                        uploadId
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7)"""
            cursor.execute(f"PREPARE stmt AS {stmt}")
            execute_batch(cursor, "EXECUTE stmt (%s, %s, %s, %s, %s, %s, %s)", csv)
            cursor.execute("DEALLOCATE stmt")
            conn.commit()
        except Exception as error:
            conn.rollback()
            print("insert_csv_to_database error", error)
            raise HTTPException(
                status_code=500, detail=f"Failed to insert file in database"
            )


def save_billing_upload_record(name: str):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO billings_uploads(name)
                        VALUES (%s)
                        RETURNING id""",
                [name],
            )
            conn.commit()
            return cursor.fetchone()[0]
        except Exception as error:
            conn.rollback()
            print("save_billing_upload_record error", error)
            raise HTTPException(
                status_code=500, detail=f"Failed to save billing upload"
            )


def update_status(id: int, status: str, table: str):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            today = datetime.now()
            updatedAt = today.isoformat()

            # try:
            cursor.execute(
                f"""UPDATE {table}
                        SET status = %s,
                            updatedAt = %s
                        WHERE id = %s""",
                (status, updatedAt, id),
            )
            conn.commit()
            return id
        except Exception as error:
            conn.rollback()
            print("update_status error", error)
            raise HTTPException(
                status_code=500, detail=f"Failed to save billing upload"
            )


def fetch_all_upload_billing_records():
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM billings_uploads")

            rows = cursor.fetchall()
            return rows
        except Exception as error:
            print("fetch_all_upload_billing_records error", error)
            raise HTTPException(status_code=500, detail=f"Failed to fetch billings")


def fetch_billing_by_upload_id(uploadId):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM billings
                        WHERE uploadId = %s""",
                (uploadId,),
            )

            return cursor.fetchall()
        except Exception as error:
            print("fetch_all_upload_billing_records error", error)
            raise HTTPException(status_code=500, detail=f"Failed to fetch billings")


def fetch_pending_billings():
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                """SELECT * FROM billings
                    WHERE status = %s""",
                ("ACKNOWLEDGED",),
            )

            return cursor.fetchall()
        except Exception as error:
            print("fetch_pending_billings error", error)


def fetch_acknowledged_uploads():
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM billings_uploads
                    WHERE status = %s""",
                ("ACKNOWLEDGED",),
            )

            return cursor.fetchall()
        except Exception as error:
            print("fetch_pending_billings error", error)


def update_many_billings_uploads_status(ids: List[int], status: str):
    with database.instance.get_connection() as conn:
        try:
            cursor = conn.cursor()
            values_to_update = [(status, id) for id in ids]
            cursor.executemany(
                "UPDATE billings_uploads SET status = %s WHERE id = %s",
                values_to_update,
            )
            conn.commit()
        except Exception as error:
            conn.rollback()
            print("update_many_billings_status error", error)
