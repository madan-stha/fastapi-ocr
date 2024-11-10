from fastapi import APIRouter, File, UploadFile
from services.file_service import save_file, get_file

router= APIRouter()

@router.post("/upload")
async def upload_file(file:UploadFile=File(...)):
  return save_file(file)

@router.get("/download/(filename:str)")
async def download_file(filename:str):
  return get_file(filename)