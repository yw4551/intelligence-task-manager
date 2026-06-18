from fastapi import APIRouter
from database.agent_db import agent
from database.mission_db import mission


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def get_summary():
    result = {}
    result["active_agents_count"] = agent.count_active_agents()
    result["total_missions"] = mission.count_all_missions()
    result["open_missions"] = mission.count_open_missions()
    result["completed_missions"] = mission.count_by_status("COMPLETED")
    result["failed_missions"] = mission.count_by_status("FAILED")
    result["critical_missions"] = mission.count_critical_missions()
    return result


@router.get("/missions-by-status")
def count_missions_by_status():
    result = {}
    result["open"] = mission.count_by_status("NEW")
    result["in_progress"] = mission.count_by_status("IN_PROGRESS")
    result["completed"] = mission.count_by_status("COMPLETED")
    result["failed"] = mission.count_by_status("FAILED")
    result["critical"] = mission.count_by_status("CANCELLED")
    return result


@router.get("/top-agent")
def get_top_agent():
    return mission.get_top_agent()
