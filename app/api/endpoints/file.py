from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services import FileService

router = APIRouter()


@router.get("/download_csv_report", response_class=FileResponse)
async def get_vacancies_csv_report():
    """Get an unloading of all jobs in csv"""
    filepath = await FileService.get_vacancies_csv_report()
    return FileResponse(filepath, media_type="application/octet-stream", filename="vacancies_report.csv")
