from fastapi import Depends, FastAPI
from auth import get_current_active_user
from routes.user import router as user_router
from routes.studentclass import router as studentclass_router


app = FastAPI(root_path="/api/v1")
app.include_router(user_router)
app.include_router(studentclass_router)
