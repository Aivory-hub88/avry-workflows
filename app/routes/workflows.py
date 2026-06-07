"""
Workflows API endpoints - Minimal implementation for dashboard
"""

import logging
from fastapi import APIRouter, HTTPException, Query, Request, Depends
from uuid import uuid4
from datetime import datetime
from typing import List, Optional

from app.database.db_service import DatabaseService
from app.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])

# File-based persistence (MVP)
db = DatabaseService(base_path="data")


@router.post("/create")
async def create_workflow(request: Request):
    """
    Create a new workflow.
    """
    try:
        data = await request.json()
        user_id = data.get("user_id")
        name = data.get("name")
        definition = data.get("definition", {})
        
        workflow_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        
        logger.info(f"Creating workflow '{name}' for user {user_id}")

        record = {
            "workflow_id": workflow_id,
            "user_id": user_id,
            "name": name,
            "definition": definition,
            "status": "created",
            "created_at": now,
            "updated_at": now,
        }
        db.save_json("workflows", workflow_id, record)

        return record
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create workflow")


@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, user_id: str = Query(...)):
    """
    Execute a workflow.
    """
    logger.info(f"Executing workflow {workflow_id} for user {user_id}")
    
    now = datetime.utcnow().isoformat()
    
    return {
        "workflow_id": workflow_id,
        "user_id": user_id,
        "status": "executing",
        "execution_id": str(uuid4()),
        "started_at": now
    }


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str, user_id: str = Query(...)):
    """
    Get workflow details.
    """
    logger.info(f"Getting workflow {workflow_id} for user {user_id}")
    
    now = datetime.utcnow().isoformat()
    
    return {
        "workflow_id": workflow_id,
        "user_id": user_id,
        "name": "Sample Workflow",
        "status": "active",
        "created_at": now
    }


@router.get("/list")
async def list_workflows(user_id: str = Query(..., description="User ID")):
    """
    List workflows for a user.
    """
    logger.info(f"Listing workflows for user: {user_id}")

    workflows = [
        w for w in db.load_all_json("workflows") if w.get("user_id") == user_id
    ]
    workflows.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return workflows


@router.get("")
async def list_all_workflows(_admin: dict = Depends(require_admin)):
    """
    List all workflows (GET /api/v1/workflows) - admin only
    
    Returns:
        List of workflow records across all users (admin view)
    """
    logger.info("Listing all workflows")

    workflows = db.load_all_json("workflows")
    workflows.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {
        "success": True,
        "workflows": workflows,
        "total": len(workflows),
        "timestamp": datetime.utcnow().isoformat(),
    }
