from fastapi import Depends, FastAPI
from auth import get_current_active_user
from routes.user import router as user_router



app = FastAPI(root_path="/api/v1")
app.include_router(user_router)
