from fastapi import APIRouter, BackgroundTasks, UploadFile, File, HTTPException
from services.billing import (
    upload_billing_csv,
    get_upload_billing_records,
)

router = APIRouter()


@router.get("/billings/csv/uploads", tags=["billing"])
async def fetch_uploaded_csv_files():
    records = await get_upload_billing_records()
    return {"records": records}


@router.post("/billings/csv/upload", tags=["billing"])
async def upload_csv_file(file: UploadFile = File(...)):
    # Check if the file is not empty
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")

    # Check if the file is a CSV
    if file.filename.endswith(".csv"):
        await upload_billing_csv(file)
        return {"message": "File uploaded and saved successfully."}

    raise HTTPException(
        status_code=400, detail="Invalid file format. Only CSV files are allowed"
    )
