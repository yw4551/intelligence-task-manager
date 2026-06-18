from database import db_connection
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from fastapi import HTTPException


class CreateAgent(BaseModel):
    name: str = Field(..., max_length=50)
    specialty: str = Field(..., max_length=50)
    agent_rank: str = Literal["Junior", "Senior", "Commander"]


class AgentDB:
    def __init__(self):
        self.connection = db_connection.DB_connection(
            "127.0.0.1", "root", "1234", "Intelligence_db", 3306
        )

    def create_agent(self, data: CreateAgent):
        try:
            sql = "INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)"
            values = (data.name, data.specialty, data.agent_rank)
            last_id, _ = self.connection.connect_to_db(sql, values)
            return self.get_agent_by_id(last_id)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def get_all_agents(self) -> list[dict]:
        sql = "SELECT * FROM agents"
        data = self.connection.fetch_all(sql)
        if not data:
            return []

        return data

    def get_agent_by_id(self, id: int) -> list[dict]:
        sql = "SELECT * FROM agents WHERE id = %s"
        values = (id, )

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")

        data = self.connection.fetch_one(sql, values)

        if not data:
            raise HTTPException(status_code=404, detail=f"Agent ID {id} not found.")
        return data

    def update_agent(self, id: int, data: CreateAgent) -> dict:
        sql = "UPDATE agents SET name = %s, specialty = %s, agent_rank = %s WHERE id = %s"
        values = (data.name, data.specialty, data.agent_rank, id)

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")

        _, count_rows = self.connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} updated successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Agent ID {id} not found.")

    def deactivate_agent(self, id: int) -> dict:
        sql = "UPDATE agents SET is_active = False WHERE id = %s"
        values = (id, )

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")
        
        agent = self.get_agent_by_id(id)
        if agent["is_active"] == False:
            raise HTTPException(status_code=400, detail=f"Agent ID {id} is not active already.")

        _, count_rows = self.connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} deactivate successfully."}
        else:
            raise HTTPException(status_code=404, detail=f"Agent ID {id} not found.")

    def increment_completed(self, id: int) -> dict:
        sql = "UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"
        values = (id, )
        _, count_rows = self.connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} completed a mission successfully."}
        else:
            return {"message": f"Failed incrementing agent {id}."}

    def increment_failed(self, id: int) -> dict:
        sql = "UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"
        values = (id, )
        _, count_rows = self.connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} failed a mission."}
        else:
            return {"message": f"Failed incrementing agent's {id} failed_missions."}

    def get_agent_performance(self, id: int) -> dict:
        sql = "SELECT completed_missions, failed_missions FROM agents WHERE id = %s"
        values = (id, )

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")

        data = self.connection.fetch_one(sql, values)

        if not data:
            raise HTTPException(status_code=404, detail=f"Agent ID {id} not found.")

        try:
            return {
                "Completed": data["completed_missions"],
                "failed": data["failed_missions"],
                "total": data["completed_missions"] + data["failed_missions"],
                "success_rate": (data["failed_missions"] / data["completed_missions"])
                * 100,
            }
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail=f"Agent ID {id} cant get the success rate.")

    def count_active_agents(self):
        sql = "SELECT COUNT(*) FROM agents WHERE is_active = %s"
        values = (True, )
        data = self.connection.fetch_one(sql, values)
        return data


agent = AgentDB()
