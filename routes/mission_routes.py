from fastapi import APIRouter
from database.mission_db import mission


router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("", status_code=201)
def create_mission(data: dict) -> dict:
    return mission.create_mission(data)


@router.get("")
def get_all_missions() -> list[dict]:
    return mission.get_all_missions()


@router.get("/{id}")
def get_mission_by_id(id: int) -> dict:
    return mission.get_mission_by_id(id)


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int, agent_id: int) -> dict:
    start_mission(id)
    return mission.assign_mission(id, agent_id)


@router.put("/{id}/start")
def start_mission(id: int) -> dict:
    return mission.update_mission_status(id, "ASSIGNED")


@router.put("/{id}/start")
def compleat_mission(id: int) -> dict:
    return mission.update_mission_status(id, "COMPLETED")


@router.put("/{id}/start")
def compleat_mission(id: int) -> dict:
    return mission.update_mission_status(id, "FAILED")


@router.put("/{id}/start")
def compleat_mission(id: int) -> dict:
    return mission.update_mission_status(id, "CANCELLED")
