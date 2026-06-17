from db_connection import connection
from pydantic import BaseModel, Field
from typing import Literal


class CreateAgent(BaseModel):
    name: str = Field(..., max_length=50)
    specialty: str = Field(..., max_length=50)
    agent_rank: str = Literal["Junior", "Senior", "Commander"]


class AgentDB:
    def create_agent(self, data: CreateAgent):
        sql = "INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s, %s)"
        values = (data.name, data.specialty, data.agent_rank)
        last_id, _ = connection.connect_to_db(sql, values)
        return self.get_agent_by_id(last_id)

    def get_all_agents(self) -> list[dict]:
        sql = "SELECT * FROM agents"
        data = connection.fetch_all(sql)
        return data

    def get_agent_by_id(self, id: int) -> list[dict]:
        sql = "SELECT * FROM agents WHERE id = %s"
        values = (id, )
        data = connection.fetch_one(sql, values)
        return data

    def update_agent(self, id: int, data: CreateAgent) -> dict:
        sql = "UPDATE agents SET name = %s, specialty = %s, agent_rank = %s WHERE id = %s"
        values = (data.name, data.specialty, data.agent_rank, id)
        _, count_rows = connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} updated successfully."}
        else:
            return {"message": f"Failed updating agent {id}."}

    def deactivate_agent(self, id: int) -> dict:
        sql = "UPDATE agents SET is_active = False WHERE id = %s"
        values = (id, )
        count_rows = connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} deactivate successfully."}
        else:
            return {"message": f"Failed deactivating agent {id}."}

    def increment_completed(self, id: int) -> dict:
        sql = "UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"
        values = (id, )
        count_rows = connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} completed a mission successfully."}
        else:
            return {"message": f"Failed incrementing agent {id}."}

    def increment_failed(self, id: int) -> dict:
        sql = "UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"
        values = (id, )
        count_rows = connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Agent {id} failed a mission."}
        else:
            return {"message": f"Failed incrementing agent's {id} failed_missions."}

    def get_agent_performance(self, id: int) -> dict:
        sql = "SELECT completed_missions, failed_missions FROM agents WHERE id = %s"
        values = (id, )
        data = connection.fetch_one(sql, values)
        return {
            "Completed": data["completed_missions"],
            "failed": data["failed"],
            "total": data["completed_missions"] + data["failed"],
            "success_rate": (data["completed_missions"] / data["failed"]) * 100
        }
    
    def count_active_agents(self):
        sql = "SELECT * FROM agents WHERE is_active = %s"
        values = (True, )
        data = connection.fetch_all(sql, values)
        return data
