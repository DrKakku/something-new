from __future__ import annotations

from typing import Iterable

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.core.database import get_session
from app.domain.repositories import FoodRepository, RecipeRepository
from app.domain.schemas import RecipeCreate, RecipeItemIn, RecipeOut, RecipeUpdate
from app.domain.services import RecipeService

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_service():
	with get_session() as session:
		service = RecipeService(RecipeRepository(session), FoodRepository(session))
		yield service


@router.post("/", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
async def create_recipe(payload: RecipeCreate, service: RecipeService = Depends(get_service)) -> RecipeOut:
	try:
		return service.create_recipe(data=payload)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{recipe_id}", response_model=RecipeOut | None)
async def get_recipe(recipe_id: int, service: RecipeService = Depends(get_service)) -> RecipeOut | None:
	return service.get_recipe(recipe_id)


@router.get("/", response_model=list[RecipeOut])
async def list_recipes(
	limit: int = Query(100, ge=1, le=500),
	offset: int = Query(0, ge=0),
	service: RecipeService = Depends(get_service),
) -> list[RecipeOut]:
	rows: Iterable[RecipeOut] = service.list_recipes(limit=limit, offset=offset)
	return list(rows)


@router.patch("/{recipe_id}", response_model=RecipeOut)
async def update_recipe(recipe_id: int, payload: RecipeUpdate, service: RecipeService = Depends(get_service)) -> RecipeOut:
	updated = service.update_recipe(recipe_id, payload)
	if updated is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
	return updated


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_recipe(recipe_id: int, service: RecipeService = Depends(get_service)) -> Response:
	deleted = service.delete_recipe(recipe_id)
	if not deleted:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{recipe_id}/items", response_model=RecipeOut)
async def add_item(recipe_id: int, payload: RecipeItemIn, service: RecipeService = Depends(get_service)) -> RecipeOut:
	updated = service.add_item(recipe_id, payload)
	if updated is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found or food missing")
	return updated


@router.patch("/{recipe_id}/items/{item_id}", response_model=RecipeOut)
async def update_item_quantity(
	recipe_id: int,
	item_id: int,
	quantity: float,
	service: RecipeService = Depends(get_service),
) -> RecipeOut:
	updated = service.update_item_quantity(recipe_id, item_id, quantity)
	if updated is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe or item not found")
	return updated


@router.delete("/{recipe_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def remove_item(recipe_id: int, item_id: int, service: RecipeService = Depends(get_service)) -> Response:
	ok = service.remove_item(recipe_id, item_id)
	if not ok:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe or item not found")
	return Response(status_code=status.HTTP_204_NO_CONTENT)
