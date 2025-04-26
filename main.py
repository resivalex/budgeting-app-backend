import budgeting_app_backend.load_env  # noqa
from fastapi import FastAPI, UploadFile, HTTPException, Request
from typing import List
from budgeting_app_backend import (
    State,
    SpendingLimitsValue,
    MonthSliceSpendingLimitsValue,
    MonthItemSpendingLimitValue,
    CategoryExpansionsValue,
    AccountPropertiesValue,
    UploadDetailsValue,
    SqliteConnection,
    SqlSettings,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.openapi.utils import get_openapi
import os
import re
import logging
from budgeting_app_backend.backup import BackupService, BackupScheduler

# Environment variables
DB_URL = os.getenv("DB_URL")
TOKEN = os.getenv("TOKEN")
PASSWORD = os.getenv("PASSWORD")
BACKEND_URL = os.getenv("BACKEND_URL")
SQLITE_PATH = os.getenv("SQLITE_PATH")
GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv("GOOGLE_DRIVE_CREDENTIALS_PATH")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

# Get the schedule configuration with defaults
DAILY_BACKUP_HOUR = int(os.getenv("DAILY_DUMP_HOUR", "3"))
DAILY_BACKUP_MINUTE = int(os.getenv("DAILY_DUMP_MINUTE", "0"))

# Create FastAPI app
app = FastAPI(docs_url="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_state() -> State:
    """
    Create and return a new State instance.
    Used as a factory for getting the application state.
    """
    sqlite_connection = SqliteConnection(sqlite_path=SQLITE_PATH)
    app_settings = SqlSettings(sql_connection=sqlite_connection)
    return State(
        sql_connection=sqlite_connection,
        db_url=DB_URL,
        settings=app_settings,
        google_drive_credentials_path=GOOGLE_DRIVE_CREDENTIALS_PATH,
        google_drive_folder_id=GOOGLE_DRIVE_FOLDER_ID
    )

# Initialize backup service with state factory
backup_service = BackupService(state_factory=create_state)

# Create backup scheduler
backup_scheduler = BackupScheduler(
    backup_service=backup_service,
    hour=DAILY_BACKUP_HOUR,
    minute=DAILY_BACKUP_MINUTE
)

# Start the scheduler on app startup
@app.on_event("startup")
def start_scheduler():
    """Start the backup scheduler when the app starts"""
    try:
        backup_scheduler.start()
    except Exception as e:
        logger.error(f"Failed to start backup scheduler: {str(e)}")

# Shut down the scheduler on app shutdown
@app.on_event("shutdown")
def shutdown_scheduler():
    """Shut down the backup scheduler when the app shuts down"""
    try:
        backup_scheduler.shutdown()
    except Exception as e:
        logger.error(f"Error shutting down backup scheduler: {str(e)}")

# Authentication
def check_authorization(request: Request):
    authorization = request.headers.get("authorization")

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header not found")

    matches = re.match(r"^Bearer ([^ ]+)$", authorization)
    if not matches:
        raise HTTPException(
            status_code=401, detail='Authorization must be in format "Bearer TOKEN"'
        )

    token = matches[1]

    if token != TOKEN:
        raise HTTPException(status_code=400, detail="Not authenticated")


# API Endpoints

@app.get("/", tags=["System"])
async def root() -> str:
    return "OK"


@app.get("/health", tags=["System"])
async def health():
    """
    Health check endpoint that also returns information about the scheduler.
    """
    return {
        "status": "healthy",
        "scheduler_running": backup_scheduler.scheduler.running,
        "next_scheduled_backup": backup_scheduler.get_next_backup_time()
    }


@app.get("/config", tags=["System"])
async def config(password: str):
    if password != PASSWORD:
        raise HTTPException(status_code=400, detail="Not authenticated")

    return {"backend_token": TOKEN, "db_url": DB_URL}


@app.get("/settings", tags=["State"])
async def settings(request: Request) -> UploadDetailsValue:
    check_authorization(request)
    return create_state().settings()


@app.get("/transactions", tags=["State"])
async def transactions(request: Request) -> List:
    check_authorization(request)
    return create_state().transactions()


@app.post("/importing", tags=["State"])
async def importing(file: UploadFile, request: Request):
    check_authorization(request)
    content = file.file.read()
    create_state().importing(content)
    return "OK"


@app.get("/exporting", tags=["State"])
async def exporting(request: Request):
    check_authorization(request)
    csv_bytes = create_state().exporting()
    return StreamingResponse(
        iter([csv_bytes]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=export.csv"},
    )


@app.post("/trigger-backup", tags=["Admin"])
async def trigger_backup(request: Request):
    """
    Manually trigger a backup to Google Drive.
    Useful for testing or for manually initiating a backup.
    """
    check_authorization(request)
    try:
        result = backup_scheduler.trigger_backup_now()
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Unknown error during backup")
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error triggering backup: {str(e)}"
        )


@app.post("/spending-limits", tags=["State"])
async def set_spending_limits(value: SpendingLimitsValue, request: Request):
    check_authorization(request)
    create_state().set_spending_limits(value)
    return "OK"


@app.get("/spending-limits", tags=["State"])
async def get_spending_limits(request: Request) -> SpendingLimitsValue:
    check_authorization(request)
    return create_state().get_spending_limits()


@app.post("/spending-limits/month-budget", tags=["State"])
async def set_budget_month_limit(
    value: MonthSliceSpendingLimitsValue, request: Request
):
    check_authorization(request)
    create_state().set_budget_month_limit(value)
    return "OK"


@app.get("/spending-limits/month-budget", tags=["State"])
async def get_budget_month_limit(
    month: str, request: Request
) -> MonthSliceSpendingLimitsValue:
    check_authorization(request)
    return create_state().get_budget_month_limit(month)


@app.post("/spending-limits/month-budget-item", tags=["State"])
async def set_budget_month_item_limit(
    value: MonthItemSpendingLimitValue, request: Request
):
    check_authorization(request)
    create_state().set_budget_month_item_limit(value)
    return "OK"


@app.post("/category-expansions", tags=["State"])
async def set_category_expansion(value: CategoryExpansionsValue, request: Request):
    check_authorization(request)
    create_state().set_category_expansions(value)
    return "OK"


@app.get("/category-expansions", tags=["State"])
async def get_category_expansion(request: Request) -> CategoryExpansionsValue:
    check_authorization(request)
    return create_state().get_category_expansions()


@app.post("/account-properties", tags=["State"])
async def set_account_properties(value: AccountPropertiesValue, request: Request):
    check_authorization(request)
    create_state().set_account_properties(value)
    return "OK"


@app.get("/account-properties", tags=["State"])
async def get_account_properties(request: Request) -> AccountPropertiesValue:
    check_authorization(request)
    return create_state().get_account_properties()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Budgeting App API",
        version="0.1.0",
        description="Budgeting App API",
        routes=app.routes,
    )
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}
    openapi_schema["components"]["securitySchemes"]["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "TOKEN",
    }
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi
