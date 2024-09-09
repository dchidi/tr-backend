from fastapi import APIRouter
# , Depends
# from typing import List
# from app.db.models import Report

# from app.services.report_service import ReportService
# from app.core.security import get_current_user

router = APIRouter()


@router.get("/test")
async def test():
    return {"msg":"test route"}


# @router.get("/reports", response_model=List[Report])
# async def get_reports(current_user: dict = Depends(get_current_user)):
#     try:
#         return await ReportService.get_all_reports()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/reports", response_model=Report)
# async def create_report(report: Report,
# current_user: dict = Depends(get_current_user)):
#     try:
#         return await ReportService.create_report(report)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/reports/{report_id}", response_model=Report)
# async def get_report(report_id: int,
# current_user: dict = Depends(get_current_user)):
#     try:
#         report = await ReportService.get_report_by_id(report_id)
#         if not report:
#             raise HTTPException(status_code=404, detail="Report not found")
#         return report
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
