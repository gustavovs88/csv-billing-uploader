from datetime import datetime
from fastapi import HTTPException
from dependencies import database


def save_single_billing(csv_row, uploadId):
    cursor = database.instance.cursor

    # try:
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
    # except:
    #     debdtId = csv_row[5]
    #     raise HTTPException(
    #         status_code=500, detail=f"Failed to save billing. debtId = {debdtId}"
    #     )


def commit():
    database.instance.connection.commit()


def save_billing_upload_record(name: str):
    cursor = database.instance.cursor

    # try:
    cursor.execute(
        """INSERT INTO billings_uploads(name)
                VALUES (%s)
                RETURNING id""",
        [name],
    )
    commit()
    return cursor.fetchone()[0]
    # except:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Failed to save billing upload record. Upload file name = {name}",
    #     )


def update_status(id: int, status: str, table: str):
    cursor = database.instance.cursor
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
    commit()
    return id
    # except:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Failed to update billing status. Upload id = {id}",
    #     )


def fetch_all_upload_billing_records():
    cursor = database.instance.cursor
    try:
        cursor.execute("SELECT * FROM billings_uploads")

        rows = cursor.fetchall()
        return database.instance.toJSON(rows)
    except:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get billing upload records.",
        )


def fetch_billing_by_upload_id(uploadId):
    cursor = database.instance.cursor
    # try:
    print(uploadId, ":::::::::::::::::::::")
    cursor.execute(
        """SELECT * FROM billings
            WHERE uploadId = %s""",
        (uploadId,),
    )

    rows = cursor.fetchall()
    return rows
    # except:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Failed to get billing upload records.",
    #     )
