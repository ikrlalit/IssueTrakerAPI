from fastapi import APIRouter, Request, HTTPException, Query,UploadFile, File
from asyncpg.exceptions import UniqueViolationError
from app.schemas import *
from app.queries import *
import bcrypt

router = APIRouter()

#--------------------------- USER APIS ---------------------------
@router.post("/users", response_model=UserResponse)
async def create_user_f(payload: UserCreate, request: Request):
    try:
        hashed_pwd = bcrypt.hashpw(
            payload.password.encode(),
            bcrypt.gensalt()
        ).decode()

        return await create_user_q(
            request.app.state.pool,
            payload.username,
            hashed_pwd,
            payload.role
        )

    except UniqueViolationError:
        raise HTTPException(status_code=409, detail="Username exists")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
    

#------------------------- ISSUES APIS -------------------------
@router.post("/issues", response_model=IssueResponse)
async def create_issue_f(payload: IssueCreate, request: Request):
    try:
        return await create_issue_q(
            request.app.state.pool,
            payload.title,
            payload.description,
            payload.priority,
            payload.assignee_id
        )
    except UniqueViolationError:
        raise HTTPException(
            status_code=409,
            detail="Issue with same title, description, priority and status already exists"
        )

@router.get("/issues", response_model=list[IssueResponse])
async def list_issues_f(
    request: Request,
    limit: int = Query(10, le=100),
    offset: int = 0,
    search_keyword: str | None = None,
):
    return await list_issues_q(
        request.app.state.pool,
        limit,
        offset,
        search_keyword

    )


@router.get("/issues/{id}", response_model=IssueDetailResponse)
async def get_issue_f(id: int, request: Request):
    issue = await get_issue_q(
        request.app.state.pool,
        id
    )
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    labels=await get_issue_labels_q(request.app.state.pool,
        id)

    issue["labels"] = (
    labels.get("labels")
    if labels and labels.get("labels") is not None
    else ""
)

    comments=await get_issue_comments_q(request.app.state.pool,
        id)
    issue['comments']=comments if comments else []
    

    return issue


@router.patch("/issues/{id}", response_model=IssueResponse)
async def update_issue_f(
    id: int,
    payload: IssueUpdate,
    request: Request
):
    issue = await update_issue_q(
        request.app.state.pool,
        id,
        payload.model_dump(exclude_unset=True)
    )

    if not issue:
        raise HTTPException(
            status_code=409,
            detail="Version conflict or issue not found"
        )

    return issue


# -----------------------ISSUES + COMMENT APIS ------------------- 
@router.post("/issues/{id}/comments")
async def add_comment_f(
    id: int,
    payload: CommentCreate,
    request: Request
):
    comment = await add_comment_q(
        request.app.state.pool,
        id,
        payload.user_id,
        payload.content
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Issue not found")
    return comment

# ---------------- Label Update Atomically ----------------
@router.put("/issues/{id}/labels")
async def replace_labels_f(
    id: int,
    payload: LabelReplace,
    request: Request
):
    result = await replace_labels_q(
        request.app.state.pool,
        id,
        payload.label_ids
    )
    if not result:
        raise HTTPException(status_code=404, detail="Issue not found")
    return {"message": "Labels replaced successfully"}

# ---------------- ISSUES BULK STATUS UPDATE API----------------
@router.post("/issues/bulk-status")
async def bulk_status_f(
    payload: BulkStatusUpdate,
    request: Request
):
    return await bulk_update_status_q(
        request.app.state.pool,
        payload.issue_ids,
        payload.status
    )

# ---------------- ISSUES DATA IMPORT WITH CSV File ----------------
@router.post("/issues/import")
async def import_issues_f(
    request: Request,
    file: UploadFile = File(...)
):
    content = (await file.read()).decode("utf-8")
    await import_issues_q(
        request.app.state.pool,
        content
    )
    return {"message": "Issues imported successfully"}

# ---------------- REPORTING APIS ----------------

@router.get(
    "/reports/top-assignees",
    response_model=list[TopAssigneeReport]
)
async def top_assignees(
    request: Request,
    limit: int = Query(5, le=20)
):
    return await get_top_assignees(
        request.app.state.pool,
        limit
    )


@router.get(
    "/reports/latency",
    response_model=LatencyReport
)
async def latency_report(request: Request):
    return await get_latency_report(
        request.app.state.pool
    )