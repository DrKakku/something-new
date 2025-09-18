from __future__ import annotations

from typing import Iterable

from app.domain.models import Food
from app.domain.repositories import FoodRepository
from app.domain.schemas import FoodCreate, FoodOut, FoodUpdate


class FoodService:
	def __init__(self, repository: FoodRepository) -> None:
		self._repository = repository

	def create_food(self, *, data: FoodCreate) -> FoodOut:
		existing = self._repository.get_by_name(name=data.name)
		if existing is not None:
			raise ValueError("Food with this name already exists")
		food = Food(
			name=data.name,
			calories=data.calories,
			protein_g=data.protein_g,
			carbs_g=data.carbs_g,
			fat_g=data.fat_g,
			fiber_g=data.fiber_g,
			sugar_g=data.sugar_g,
			saturated_fat_g=data.saturated_fat_g,
			sodium_mg=data.sodium_mg,
			potassium_mg=data.potassium_mg,
			cholesterol_mg=data.cholesterol_mg,
			additional_nutrients=data.additional_nutrients,
			serving_size=data.serving_size,
			serving_unit=data.serving_unit,
			grams_per_ml=data.grams_per_ml,
		)
		food = self._repository.create(obj_in=food)
		return FoodOut.model_validate(food)

	def get_food(self, *, food_id: int) -> FoodOut | None:
		food = self._repository.get_by_id(food_id=food_id)
		return None if food is None else FoodOut.model_validate(food)

	def list_foods(self, *, limit: int = 100, offset: int = 0) -> Iterable[FoodOut]:
		rows = self._repository.list_all(limit=limit, offset=offset)
		return (FoodOut.model_validate(row) for row in rows)

	def update_food(self, *, food_id: int, data: FoodUpdate) -> FoodOut | None:
		food = self._repository.get_by_id(food_id=food_id)
		if food is None:
			return None
		for field_name, value in data.model_dump(exclude_unset=True).items():
			setattr(food, field_name, value)
		return FoodOut.model_validate(food)

	def delete_food(self, *, food_id: int) -> bool:
		return self._repository.delete(food_id=food_id)
