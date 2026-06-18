from database import db_connection
from pydantic import BaseModel, Field, ValidationError
from database.agent_db import agent
from fastapi import HTTPException

class MissionCreate(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(...)
    location: str = Field(..., max_length=100)
    difficulty: int = Field(..., ge=1, le=10)
    importance: int = Field(..., ge=1, le=10)


class MissionDB:
    def __init__(self):
        self.connection = db_connection.DB_connection(
            "127.0.0.1", "root", "1234", "Intelligence_db", 3306
        )

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

    def create_mission(self, data: MissionCreate) -> dict:
        try:
            sql = "INSERT INTO missions (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (
                data.title,
                data.description,
                data.location,
                data.difficulty,
                data.importance,
                self.get_risk_level(data.difficulty, data.importance)
            )

            last_id, _ = self.connection.connect_to_db(sql, values)
            return self.get_mission_by_id(last_id)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")
        except KeyError as e:
            raise HTTPException(status_code=422, detail=f"Error: {e}")

    def get_all_missions(self) -> list[dict]:
        sql = "SELECT * FROM missions"
        data = self.connection.fetch_all(sql)
        return data

    def get_mission_by_id(self, id: int) -> list[dict]:
        sql = "SELECT * FROM missions WHERE id = %s"
        values = (id,)

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")

        data = self.connection.fetch_one(sql, values)

        if not data:
            raise HTTPException(status_code=404, detail=f"Mission {id} not found.")

        return data

    def assign_mission(self, m_id: int, a_id: int) -> dict:
        sql = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
        values = (a_id, m_id)

        agent_dict = agent.get_agent_by_id(a_id)
        if not agent_dict["is_active"]:
            raise HTTPException(status_code=400, detail=f"Agent ID {a_id} is not active.")

        if self.get_open_missions_by_agent(a_id) == 3:
            raise HTTPException(status_code=400, detail=f"Agent ID {a_id} has too many missions.")

        mission_dict = self.get_mission_by_id(m_id)
        if mission_dict["risk_level"] == "CRITICAL" and agent_dict["agent_rank"] != "Commander":
            raise HTTPException(status_code=400, detail=f"Agent ID {a_id} can't get this mission.")

        _, count_rows = self.connection.connect_to_db(sql, values)

        if count_rows:
            return {"message": f"Mission {m_id} assigned to agent {a_id} successfully."}
        else:
            return {"message": f"Failed assigning mission {m_id} to agent {a_id}."}

    def get_status_by_id(self, id: int) -> str:
        sql = "SELECT status FROM missions WHERE id = %s"
        values = (id, )

        if not isinstance(id, int):
            raise HTTPException(status_code=422, detail="Invalid ID.")

        data = self.connection.connect_to_db(sql, values)
        return data

    def update_mission_status(self, id: int, status: str) -> dict:
        actual_status = self.get_status_by_id(id)

        if (
            (actual_status == "NEW" and status == "ASSIGNED")
            or (actual_status == "ASSIGNED" and status == "IN_PROGRESS")
            or (actual_status == "IN_PROGRESS" and status in ["COMPLETED", "FAILED", "CANCELLED"])
            or (actual_status in ["NEW", "ASSIGNED"] and status == "CANCELLED")
            ):
            sql = "UPDATE missions SET status = %s WHERE id = %s"
            values = (status, id)

            if not isinstance(id, int):
                raise HTTPException(status_code=422, detail="Invalid ID.")

            _, count_rows = self.connection.connect_to_db(sql, values)

            if count_rows:
                return {"message": f"Status of mission {id} updated successfully."}
            else:
                raise HTTPException(status_code=404, detail=f"Mission {id} not found.")
        else:
            raise HTTPException(status_code=400, detail="Illegal assignment.")

    def get_open_missions_by_agent(self, id: int) -> list[dict]:
        sql = "SELECT * FROM missions WHERE id = %s AND status = %s or status = %s"
        values = (id, "ASSIGNED", "IN_PROGRESS")
        data = self.connection.fetch_all(sql, values)
        return data

    def count_all_missions(self) -> int:
        sql = "SELECT COUNT(*) FROM missions"
        return self.connection.fetch_one(sql)

    def count_by_status(self, status: str) -> int:
        sql = "SELECT COUNT(*) FROM missions WHERE status = %s"
        values = (status, )
        return self.connection.fetch_one(sql, values)

    def count_open_missions(self):
        sql = "SELECT COUNT(*) FROM missions WHERE status IN (%s, %s, %s)"
        values = ("NEW", "ASSIGNED", "IN_PROGRESS")
        return self.connection.fetch_one(sql, values)

    def count_critical_missions(self):
        sql = "SELECT COUNT(*) FROM missions WHERE risk_level = %s"
        values = ("CRITICAL", )
        return self.connection.fetch_one(sql, values)

    def get_top_agent(self):
        sql = "SELECT * FROM agents ORDER BY completed_missions"
        result = self.connection.fetch_one(sql)
        if not result:
            raise HTTPException(status_code=404, detail="Error top agent not found.")
        return result


mission = MissionDB()
