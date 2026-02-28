from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_route import auth_router
from src.routes.order_route import order_router
from src.config.database import Base,engine


app = FastAPI(
    title="Pizza delivery project",
    summary = " This API is for tracking the order status of pizza"
)
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

app.include_router(auth_router, prefix= "/api/v1/auth", tags={"Authentification"})
app.include_router(order_router, prefix= "/api/v1/order", tags={"Order"})

@app.get('/')
async def home():
    """Landing Page"""
    return "welcome to our api"