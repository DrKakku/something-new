from __future__ import annotations

from typing import Iterable

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.database import get_session
from app.domain.repositories import FoodRepository
from app.domain.schemas import FoodCreate, FoodOut, FoodUpdate
from app.domain.services import FoodService

router = APIRouter(prefix="/foods", tags=["foods"])


def get_service():
	with get_session() as session:
		repo = FoodRepository(session)
		yield FoodService(repo)


@router.post("/", response_model=FoodOut, status_code=status.HTTP_201_CREATED)
async def create_food(payload: FoodCreate, service: FoodService = Depends(get_service)) -> FoodOut:
	try:
		return service.create_food(data=payload)
	except ValueError as exc:  # duplicate
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{food_id}", response_model=FoodOut | None)
async def get_food(food_id: int, service: FoodService = Depends(get_service)) -> FoodOut | None:
	return service.get_food(food_id=food_id)


@router.get("/", response_model=list[FoodOut])
async def list_foods(
	limit: int = Query(100, ge=1, le=500),
	offset: int = Query(0, ge=0),
	service: FoodService = Depends(get_service),
) -> list[FoodOut]:
	rows: Iterable[FoodOut] = service.list_foods(limit=limit, offset=offset)
	return list(rows)


@router.patch("/{food_id}", response_model=FoodOut)
async def update_food(food_id: int, payload: FoodUpdate, service: FoodService = Depends(get_service)) -> FoodOut:
	updated = service.update_food(food_id=food_id, data=payload)
	if updated is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
	return updated


@router.delete("/{food_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_food(food_id: int, service: FoodService = Depends(get_service)) -> Response:
	deleted = service.delete_food(food_id=food_id)
	if not deleted:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
	return Response(status_code=status.HTTP_204_NO_CONTENT)
