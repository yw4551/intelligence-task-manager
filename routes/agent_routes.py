from fastapi import APIRouter
from database.agent_db import agent, CreateAgent


router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("", status_code=201)
def create_new_agent(data: CreateAgent) -> dict:
    return agent.create_agent(data)


@router.get("")
def get_all_agents_list() -> list[dict]:
    return agent.get_all_agents()


@router.get("/{id}")
def get_agent_dict_by_id(id: int) -> dict:
    return agent.get_agent_by_id(id)


@router.put("/{id}")
def update_agent(id: int, data: CreateAgent) -> dict:
    return agent.update_agent(id, data)


@router.put("/{id}/deactivate")
def deactivate_agent(id: int) -> dict:
    return agent.deactivate_agent(id)


@router.get("/{id}/performance")
def agent_deactivate(id: int) -> dict:
    return agent.get_agent_performance(id)
