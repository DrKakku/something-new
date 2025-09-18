from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Food, Recipe, RecipeItem


class RecipeRepository:
	def __init__(self, session: Session) -> None:
		self._session = session

	def create_recipe(self, recipe: Recipe) -> Recipe:
		self._session.add(recipe)
		self._session.flush()
		return recipe

	def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
		return self._session.get(Recipe, recipe_id)

	def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
		stmt = select(Recipe).where(Recipe.name == name)
		return self._session.scalar(stmt)

	def list_recipes(self, *, limit: int = 100, offset: int = 0) -> Iterable[Recipe]:
		stmt = select(Recipe).offset(offset).limit(limit)
		return self._session.scalars(stmt)

	def delete_recipe(self, recipe_id: int) -> bool:
		recipe = self.get_recipe(recipe_id)
		if recipe is None:
			return False
		self._session.delete(recipe)
		return True

	def add_item(self, *, recipe: Recipe, food: Food, quantity: float) -> RecipeItem:
		item = RecipeItem(recipe=recipe, food_id=food.id, quantity=quantity)
		self._session.add(item)
		self._session.flush()
		return item

	def update_item_quantity(self, *, item: RecipeItem, quantity: float) -> RecipeItem:
		item.quantity = quantity
		return item

	def remove_item(self, *, item: RecipeItem) -> None:
		self._session.delete(item)

	def get_item(self, *, recipe_id: int, item_id: int) -> Optional[RecipeItem]:
		return self._session.get(RecipeItem, item_id)

	def iter_items(self, *, recipe: Recipe) -> Iterable[RecipeItem]:
		stmt = select(RecipeItem).where(RecipeItem.recipe_id == recipe.id)
		return self._session.scalars(stmt)
