from __future__ import annotations

from typing import Dict, Iterable, Optional

from app.core.units import to_serving_multiplier
from app.domain.models import Food, Recipe, RecipeItem
from app.domain.repositories import FoodRepository, RecipeRepository
from app.domain.schemas import (
	RecipeCreate,
	RecipeItemIn,
	RecipeItemOut,
	RecipeOut,
	RecipeUpdate,
)


class RecipeService:
	def __init__(self, recipe_repo: RecipeRepository, food_repo: FoodRepository) -> None:
		self._recipes = recipe_repo
		self._foods = food_repo

	def _recalculate_totals(self, recipe: Recipe) -> None:
		# Reset totals
		recipe.calories = 0
		recipe.protein_g = 0.0
		recipe.carbs_g = 0.0
		recipe.fat_g = 0.0
		recipe.fiber_g = 0.0
		recipe.sugar_g = 0.0
		recipe.saturated_fat_g = 0.0
		recipe.sodium_mg = 0.0
		recipe.potassium_mg = 0.0
		recipe.cholesterol_mg = 0.0
		merged_additional: Dict[str, float] = {}

		items = list(self._recipes.iter_items(recipe=recipe))
		for item in items:
			food: Optional[Food] = self._foods.get_by_id(food_id=item.food_id)
			if food is None:
				continue
			mult = to_serving_multiplier(
				quantity=item.quantity,
				unit=item.unit,  # type: ignore[arg-type]
				food_serving_size=food.serving_size,
				food_serving_unit=food.serving_unit,  # type: ignore[arg-type]
				grams_per_ml=food.grams_per_ml,
			)
			recipe.calories += int(round(food.calories * mult))
			recipe.protein_g += food.protein_g * mult
			recipe.carbs_g += food.carbs_g * mult
			recipe.fat_g += food.fat_g * mult
			recipe.fiber_g += food.fiber_g * mult
			recipe.sugar_g += food.sugar_g * mult
			recipe.saturated_fat_g += food.saturated_fat_g * mult
			recipe.sodium_mg += food.sodium_mg * mult
			recipe.potassium_mg += food.potassium_mg * mult
			recipe.cholesterol_mg += food.cholesterol_mg * mult
			for k, v in food.additional_nutrients.items():
				merged_additional[k] = merged_additional.get(k, 0.0) + (v * mult)

		# Merge recipe-level additional nutrients (manual overrides) additively
		for k, v in (recipe.additional_nutrients or {}).items():
			merged_additional[k] = merged_additional.get(k, 0.0) + v

		recipe.additional_nutrients = merged_additional

	def _per_serving(self, recipe: Recipe) -> Dict[str, float]:
		if recipe.servings <= 0:
			return {}
		s = recipe.servings
		return {
			"calories": round(recipe.calories / s, 2),
			"protein_g": round(recipe.protein_g / s, 2),
			"carbs_g": round(recipe.carbs_g / s, 2),
			"fat_g": round(recipe.fat_g / s, 2),
			"fiber_g": round(recipe.fiber_g / s, 2),
			"sugar_g": round(recipe.sugar_g / s, 2),
			"saturated_fat_g": round(recipe.saturated_fat_g / s, 2),
			"sodium_mg": round(recipe.sodium_mg / s, 2),
			"potassium_mg": round(recipe.potassium_mg / s, 2),
			"cholesterol_mg": round(recipe.cholesterol_mg / s, 2),
			**{k: round(v / s, 2) for k, v in (recipe.additional_nutrients or {}).items()},
		}

	def _to_out(self, recipe: Recipe) -> RecipeOut:
		return RecipeOut(
			id=recipe.id,
			name=recipe.name,
			calories=recipe.calories,
			protein_g=recipe.protein_g,
			carbs_g=recipe.carbs_g,
			fat_g=recipe.fat_g,
			fiber_g=recipe.fiber_g,
			sugar_g=recipe.sugar_g,
			saturated_fat_g=recipe.saturated_fat_g,
			sodium_mg=recipe.sodium_mg,
			potassium_mg=recipe.potassium_mg,
			cholesterol_mg=recipe.cholesterol_mg,
			additional_nutrients=recipe.additional_nutrients or {},
			servings=recipe.servings,
			serving_unit=recipe.serving_unit,
			per_serving=self._per_serving(recipe),
			items=[
				RecipeItemOut(id=i.id, food_id=i.food_id, quantity=i.quantity, unit=i.unit)
				for i in self._recipes.iter_items(recipe=recipe)
			],
		)

	def create_recipe(self, data: RecipeCreate) -> RecipeOut:
		if self._recipes.get_recipe_by_name(name=data.name) is not None:
			raise ValueError("Recipe with this name already exists")
		recipe = Recipe(
			name=data.name,
			additional_nutrients=data.additional_nutrients,
			servings=data.servings,
			serving_unit=data.serving_unit,
		)
		recipe = self._recipes.create_recipe(recipe)
		for item in data.items:
			self._add_item_internal(recipe=recipe, item=item)
		self._recalculate_totals(recipe)
		return self._to_out(recipe)

	def get_recipe(self, recipe_id: int) -> Optional[RecipeOut]:
		recipe = self._recipes.get_recipe(recipe_id)
		if recipe is None:
			return None
		self._recalculate_totals(recipe)
		return self._to_out(recipe)

	def list_recipes(self, *, limit: int = 100, offset: int = 0) -> Iterable[RecipeOut]:
		rows = self._recipes.list_recipes(limit=limit, offset=offset)
		for r in rows:
			self._recalculate_totals(r)
			yield self._to_out(r)

	def update_recipe(self, recipe_id: int, data: RecipeUpdate) -> Optional[RecipeOut]:
		recipe = self._recipes.get_recipe(recipe_id)
		if recipe is None:
			return None
		for field_name, value in data.model_dump(exclude_unset=True).items():
			setattr(recipe, field_name, value)
		self._recalculate_totals(recipe)
		return self._to_out(recipe)

	def delete_recipe(self, recipe_id: int) -> bool:
		return self._recipes.delete_recipe(recipe_id)

	def _add_item_internal(self, *, recipe: Recipe, item: RecipeItemIn) -> RecipeItem:
		food = self._foods.get_by_id(food_id=item.food_id)
		if food is None:
			raise ValueError("Food not found")
		rec_item = self._recipes.add_item(recipe=recipe, food=food, quantity=item.quantity)
		rec_item.unit = item.unit
		return rec_item

	def add_item(self, recipe_id: int, item: RecipeItemIn) -> Optional[RecipeOut]:
		recipe = self._recipes.get_recipe(recipe_id)
		if recipe is None:
			return None
		self._add_item_internal(recipe=recipe, item=item)
		self._recalculate_totals(recipe)
		return self._to_out(recipe)

	def update_item_quantity(self, recipe_id: int, item_id: int, quantity: float) -> Optional[RecipeOut]:
		recipe = self._recipes.get_recipe(recipe_id)
		if recipe is None:
			return None
		item = self._recipes.get_item(recipe_id=recipe_id, item_id=item_id)
		if item is None or item.recipe_id != recipe.id:
			return None
		self._recipes.update_item_quantity(item=item, quantity=quantity)
		self._recalculate_totals(recipe)
		return self._to_out(recipe)

	def remove_item(self, recipe_id: int, item_id: int) -> bool:
		recipe = self._recipes.get_recipe(recipe_id)
		if recipe is None:
			return False
		item = self._recipes.get_item(recipe_id=recipe_id, item_id=item_id)
		if item is None or item.recipe_id != recipe.id:
			return False
		self._recipes.remove_item(item=item)
		self._recalculate_totals(recipe)
		return True
