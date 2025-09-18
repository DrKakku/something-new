from fastapi import APIRouter

from app.api.v1.food import router as food_router
from app.api.v1.recipe import router as recipe_router
from app.api.v1.seed import router as seed_router

api_v1_router = APIRouter()
api_v1_router.include_router(food_router)
api_v1_router.include_router(recipe_router)
api_v1_router.include_router(seed_router)
