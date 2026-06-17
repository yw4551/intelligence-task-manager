# Intelligence Task Manager

## About

The project is a system that manages the tasks of an intelligence unit named ShadowNet.  
The system handles the tasks and agents in the unit and manages there missions.  
This system uses the following technologies:
- MySQL
- OOP
- Docker

<br>

## File Structure

```text
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

<br>

## Table Structure

### Agents

| **Property** | **Type** | **Default** | **Comments** |
| :---: | :---: | :---: | :---: |
| id | INT || AUTO_INCREMENT, PRIMARY KEY |
| name | VARCHAR(50) || NOT NULL|
| specialty | VARCHAR(50) || NOT NULL |
| is_active | BOOLEAN | TRUE | NOT NULL |
| completed_missions | INT | 0 | NOT NULL|
| failed_missions | INT | 0 | NOT NULL |
| agent_rank | ENUM || Junior / Senior / Commander, NOT NULL |

---

### missions

| **Property** | **Type** | **Default** | **Comments** |
| :---: | :---: | :---: | :---: |
| id | INT || AUTO_INCREMENT, PRIMARY KEY |
| title | VARCHAR(50) || NOT NULL |
| description | TEXT || NOT NULL |
| location | VARCHAR(100) || NOT NULL |
| difficulty | INT || 1 - 10, NOT NULL |
| importance | INT || 1 - 10, NOT NULL |
| status | ENUM | NEW | NEW, IN_PROGRESS, COMPLETED, FAILED, CANCELLED |
| risk_level | VARCHAR(30) || LOW, MEDIUM, HIGH, CRITICAL |
| assigned_agent_id | INT | NULL ||

---
<br>

## Classes

### DbConnection

This class manages the connection with the database with the following methods:

- **get_connection** - Returns an active connection with the DB.
- **create_database** - Creates the DB if it doesn't exists.
- **create_table** - Creates both tables if they don't exist.

### AgentDB

Manages all the connections with the agents table:

- **create_agent(data)** - Creates a new agent and returns the agents object.
- **get_all_agents()** - Returns a list of all agents.
- **get_agent_by_id(id)** - Returns the selected agent or None if it doesn't exist.
- **update_agent(id, data)** - Updates a agent line and returns a success/failure message.
- **deactivate_agent(id)** - Deactivates an agent and returns a success/failure message.
- **increment_completed(id)** - Adds a completed mission to the completed missions and returns a success/failure message.
- **increment_failed(id)** - Adds a failure mission to the failed missions and returns a success/failure message.
- **get_agent_performance(id)** - Returns a dict with the num of completed and failed and total and success_rate of the agent
- **count_active_agents()** - Returns the number of active agents are there.

### MissionDB

Manages all the connections with the missions table:

- **create_mission(data)** - Creates a new mission and returns the mission object.
- **get_all_missions()** - Returns a list of all missions.
- **get_mission_by_id(id)** - Returns the selected mission or None if it doesn't exist.
- **assign_mission(m_id, a_id)** - Assigns a mission to a agent and returns a success/failure message.
- **update_mission_status(id, status)** - Updates the status of the mission to any status and returns a success/failure message.
- **get_open_missions_by_agent(id)** - Returns any mission of an agent thats marked as ASSIGNED/IN_PROGRESS.
- **count_all_missions()** - Returns the number of missions that are in the table.
- **count_by_status(status)** - Returns the amount of statuses that have a selected status.
- **count_open_missions()** - Returns the amount of missions that are open.
- **count_critical_missions()** - Returns the amount of missions that are marked as CRITICAL.
- **get_top_agent()** - Returns the agent with the most of completed_missions.

---
<br>


## System Rules

1. The agent's agent_rank most be one of the following and if not it should return an error:
    - Junior
    - Senior
    - Commander
2. The importance and difficulty most be a number between 1 to 10 otherwise it should return an error.
3. The risk_level is calculated automatically by the computer and the user doesn't need to give this data.
4. An agent that is not active can not receive a mission.
5. An agent can't have more then 3 opened missions at once.
6. If the risk_level is CRITICAL only a commander can get that mission.
7. A mission can only start with a status NEW and only after assignment it can change to assigned.
8. A mission can get a status of IN_PROGRESS only if it is in a status of assigned.
9. A mission can be marked as completed only if it was in status of IN_PROGRESS.
10. You can cancel a mission only in status of NEW or ASSIGNED otherwise it will return an error.

---
<br>

## Run Docker

To run the docker container required for this project run the following command in the terminal:

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```