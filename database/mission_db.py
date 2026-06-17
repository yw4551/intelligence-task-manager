from db_connection import connection
from pydantic import BaseModel, Field
from typing import Literal


class MissionCreate(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(...)
    location: str = Field(..., max_length=100)
    difficulty: int = Field(ge=1, le=10)
    importance: int = Field(ge=1, le=10)
    risk_level: int = difficulty * 2 + importance


class MissionDB:
    def get_risk_level(self, difficulty: int, importance: int) -> str:
        total = difficulty * 2 + importance
        if total <= 9:
            result = "LOW"
        elif total <= 17:
            result = "MEDIUM"
        elif total <= 24:
            result = "HIGH"
        else:
            result = "CRITICAL"

        return result

    def create_mission(self, data: dict) -> dict:
        sql = "INSERT INTO agents (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            data.title,
            data.description,
            data.location,
            data.difficulty,
            data.importance,
            self.get_risk_level(data.difficulty, data.importance)
        )
        last_id, _ = connection.connect_to_db(sql, values)
        return self.get_mission_by_id(last_id)

    def get_all_missions(self) -> list[dict]:
        sql = "SELECT * FROM missions"
        data = connection.fetch_all(sql)
        return data

    def get_mission_by_id(self, id: int) -> list[dict]:
        sql = "SELECT * FROM missions WHERE id = %s"
        values = (id,)
        data = connection.fetch_one(sql, values)
        return data

    def assign_mission(self, m_id: int, a_id: int) -> dict:
        sql = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
        values = (a_id, m_id)
        _, count_rows = connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Mission {m_id} assigned to agent {a_id} successfully."}
        else:
            return {"message": f"Failed assigning mission {m_id} to agent {a_id}."}

    def get_status_by_id(self, id: int) -> str:
        sql = "SELECT status FROM missions WHERE id = %s"
        values = (id, )
        data = connection.connect_to_db(sql, values)
        return data

    def update_mission_status(self, id: int, status: str) -> dict:
        actual_status = self.get_status_by_id(id)

        if (
            (actual_status == "NEW" and status == "ASSIGNED")
            or (actual_status == "ASSIGNED" and status == "IN_PROGRESS")
            or (
                actual_status == "IN_PROGRESS"
                and status in ["COMPLETED", "FAILED", "CANCELLED"]
            )
        ):
            sql = "UPDATE missions SET status = %s WHERE id = %s"
            values = (status, id)
            _, count_rows = connection.connect_to_db(sql, values)

            if count_rows:
                return {"message": f"Status of mission {id} updated successfully."}
            else:
                return {"message": f"Failed to update mission {id} status."}
        else:
            return {"message": "Illegal status update"}

    def get_open_missions_by_agent(id):
        sql = "SELECT * FROM missions WHERE id = %s AND status = %s or status = %s"
        values = (id, "ASSIGNED", "IN_PROGRESS")
        data = connection.fetch_all(sql, values)
        return data

    def count_all_missions():
        pass

    def count_by_status(status):
        pass

    def count_open_missions():
        pass

    def count_critical_missions():
        pass

    def get_top_agent():
        pass
