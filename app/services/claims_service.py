# from typing import List, Optional
# from app.db.models import Report
# from app.db.session import get_db


class ClaimService:
    pass
    # @staticmethod
    # async def get_all_reports() -> List[Report]:
    #     async with get_db() as session:
    #         return await session.execute("SELECT * FROM reports")

    # @staticmethod
    # async def create_report(report: Report) -> Report:
    #     async with get_db() as session:
    #         session.add(report)
    #         await session.commit()
    #         return report

    # @staticmethod
    # async def get_report_by_id(report_id: int) -> Optional[Report]:
    #     async with get_db() as session:
    #         result = await session.execute(
    #             "SELECT * FROM reports WHERE id = :id", {"id": report_id}
    #         )
    #         return result.fetchone()
