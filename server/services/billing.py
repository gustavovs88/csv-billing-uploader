import csv
from functools import wraps
from io import StringIO
from fastapi import UploadFile
from repositories import billing as repository
import threading

cron_job_running = False
background_job_running = False


async def upload_billing_csv(file: UploadFile):
    print(f":: Start uploading csv file {file.filename}")
    contents = await file.read()
    csv_data = contents.decode("utf-8")
    csv_reader = csv.reader(StringIO(csv_data))
    next(csv_reader)  # Skip the header row.
    uploadId = repository.save_billing_upload_record(file.filename)
    csv_list = list(tuple([*line, uploadId]) for line in csv_reader)
    repository.insert_csv_to_database(csv_list)
    print(f":: csv file {file.filename} uploaded succesfully")
    return uploadId


async def get_upload_billing_records():
    records = repository.fetch_all_upload_billing_records()
    return records


def issue_receipts_for_uploaded_file(uploadId: int):
    global cron_job_running
    global background_job_running
    if not cron_job_running and not background_job_running:
        print(f":: Start issuing receipts for uploaded file. Upload id: {uploadId}")

        background_job_running = True
        try:
            billings = repository.fetch_billing_by_upload_id(uploadId)
            for row in billings:
                ## Emite o boleto para cada registro
                ## Envia notificação para o email
                ## Atualiza status da cobrança no banco
                repository.update_status(row[0], "SENT", "billings")
            # Atualiza status do registro de upload.
            repository.update_status(uploadId, "SENT", "billings_uploads")
            print(
                f":: Receipts for uploaded file issued succesfully. Upload id: {uploadId}"
            )

        except Exception as error:
            print(
                f":: Issuing receipts for uploaded file failed. Upload id: {uploadId}, error: {error}"
            )
        finally:
            background_job_running = False
    else:
        print(
            "Background or cron job is running. issue_receipts_for_uploaded_file canceled."
        )


def issue_receipts_in_thread(uploadId):
    threading.Thread(target=issue_receipts_for_uploaded_file(uploadId)).start()


def issue_receipts_cron_job():
    global cron_job_running
    global background_job_running
    if not cron_job_running and not background_job_running:
        print(f":: Start issuing pending receipts.")
        cron_job_running = True
        try:
            billings = repository.fetch_pending_billings()
            for row in billings:
                ## Emite o boleto para cada registro
                ## Envia notificação para o email
                ## Atualiza status da cobrança no banco
                repository.update_status(row[0], "SENT", "billings")
            # Atualiza status do registro de upload.
            updated_billings_uploads = repository.fetch_acknowledged_uploads()
            repository.update_many_billings_uploads_status(
                updated_billings_uploads, "SENT"
            )
            print(f":: Pending receipts issued succesfully.")

        except Exception as error:
            print(f":: Pending receipts issuing failed. Error: {error}")
        finally:
            cron_job_running = False
    else:
        print("Background or cron job is running. issue_receipts_cron_job canceled.")


def issue_pending_receipts_in_thread():
    threading.Thread(target=issue_receipts_cron_job()).start()
