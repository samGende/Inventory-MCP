from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil

app = FastAPI()

# Where all uploaded purchase-order files will live
UPLOAD_DIR = Path("POs")
UPLOAD_DIR.mkdir(exist_ok=True)               # creates POs/ if it isn’t there already

@app.get("/test")
async def test_endpoint():
    """
    A simple test endpoint to verify that the server is running.
    """
    return {"message": "Server is running!"}

@app.post("/po")
async def upload_po(file: UploadFile = File(...)):
    """
    Accepts a single file upload and saves it under POs/<original filename>.
    """
    dest_path = UPLOAD_DIR / file.filename

    try:
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)   # stream upload → disk
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {exc}")
    finally:
        await file.close()

    return {"filename": file.filename, "saved_to": str(dest_path)}