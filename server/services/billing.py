import csv
from datetime import datetime
from io import StringIO
from fastapi import UploadFile
from repositories import billing as repository


async def upload_billing_csv(file: UploadFile):
    contents = await file.read()
    csv_data = contents.decode("utf-8")
    csv_reader = csv.reader(StringIO(csv_data))
    next(csv_reader)  # Skip the header row if it exists
    uploadId = repository.save_billing_upload_record(file.filename)
    for row in csv_reader:
        repository.save_single_billing(row, uploadId)
    repository.commit()  # commit only after all billings insert operations from csv are done
    return repository.update_status(uploadId, "SAVED", "billings_uploads")


async def get_upload_billing_records():
    records = repository.fetch_all_upload_billing_records()
    return records


async def issue_receipts(uploadId: int):
    billings = repository.fetch_billing_by_upload_id(uploadId)
    for row in billings:
        ## Emite o boleto para cada registro
        ## Envia notificação para o email
        ## Atualiza status da cobrança no banco
        print(row)
    # Atualiza status do registro de upload.
    return repository.update_status(uploadId, "SENT", "billings_uploads")
