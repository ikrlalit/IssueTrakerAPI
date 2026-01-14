# 🐞 Issue Tracker API

A **production-grade Issue Tracking backend** built with **FastAPI**, **PostgreSQL**, and **asyncpg**.

---

## 🚀 Features

### Core Functionality
- **Issue Management:** Create, update, and fetch issues with UUIDs for security.
- **Partial Updates:** Smart `PATCH` updates using Pydantic's `exclude_unset` logic.
- **Collaboration:** Assign issues to users and add threaded comments.
- **Atomic Operations:** Add and replace labels or update bulk statuses within SQL transactions.
- **Data Ingestion:** CSV import functionality for bulk issue creation.

### Reporting & Analytics
- **Top Assignees:** Identify workload distribution across the team.
- **Resolution Latency:** Calculate average time taken to resolve issues for performance metrics.

---

## 🏗️ Tech Stack

| Layer | Technology | Key Benefit |
|:---|:---|:---|
| **API Framework** | FastAPI | High performance & automatic OpenAPI docs. |
| **Database** | PostgreSQL | Relational integrity and advanced indexing. |
| **DB Driver** | asyncpg | High-speed, non-blocking PostgreSQL interface. |
| **SQL Style** | Raw SQL | Full control over query optimization (No ORM). |
| **Async Model** | asyncio | Concurrent request handling for high scalability. |
| **Validation** | Pydantic | Strict type safety and schema enforcement. |
| **Security** | bcrypt | Industry-standard password hashing. |

---

## 📁 Project Structure

```text
ISSUETRACKERAPI/
├── app/
│   ├── apis.py           # API route definitions
│   ├── db.py             # Async DB connection pooling  
│   ├── helper.py         # Contains helper function used
│   ├── schemas.py        # Pydantic request/response models
│   └── queries.py        # Optimized Raw SQL queries
├── main.py               # Application entry point
├── issues_sample.csv     # Sample file to test csv import              
└── README.md
```
---

## 🔗 Main API Endpoints

### Issues
* `POST /issues` — Create a new issue
* `GET /issues` — List all issues with filters
* `GET /issues/{id}` — Get issue with comments & labels
* `PATCH /issues/{id}` — Partial update of an issue
* `POST /issues/bulk-status` — Batch update status for multiple issues
* `POST /issues/import` — Bulk creation via CSV import

### Collaboration & Reports
* `POST /issues/{id}/comments` — Add a comment to an issue
* `PUT /issues/{id}/labels` — Atomic label replacement
* `GET /reports/top-assignees` — Fetch workload distribution
* `GET /reports/latency` — Resolution speed metrics

---

## 🔐 Security & Best Practices

* **ID Masking:** **UUIDs** are used in public APIs instead of auto-incrementing integers to prevent ID enumeration attacks.
* **SQL Injection Defense:** All database interactions use **parameterized queries** via `asyncpg`.
* **Concurrency:** Managed **connection pooling** to prevent database exhaustion under heavy load.
* **Validation:** Strict schema enforcement and data sanitization via **Pydantic**.

---

## 🚀 Running the Project

### 1. Install dependencies
```bash
pip install fastapi uvicorn asyncpg bcrypt
