from fastapi import FastAPI
from routes import agent_routes, mission_routes, report_routes


app = FastAPI()


app.include_router(agent_routes)
app.include_router(mission_routes)
app.include_router(report_routes)
