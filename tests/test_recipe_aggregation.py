from __future__ import annotations

from app.core.database import Base, SessionLocal, engine
from app.domain.models import Food
from app.domain.repositories import FoodRepository, RecipeRepository
from app.domain.schemas import RecipeCreate, RecipeItemIn
from app.domain.services import RecipeService


def setup_module(module):
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)


def test_recipe_aggregation_and_per_serving():
	with SessionLocal() as session:
		food_repo = FoodRepository(session)
		recipe_repo = RecipeRepository(session)
		service = RecipeService(recipe_repo, food_repo)

		chicken = Food(
			name="Chicken 100g",
			calories=165,
			protein_g=31,
			carbs_g=0,
			fat_g=3.6,
			serving_size=100,
			serving_unit="g",
		)
		food_repo.create(obj_in=chicken)

		olive_oil = Food(
			name="Olive Oil ml",
			calories=119,
			protein_g=0,
			carbs_g=0,
			fat_g=13.5,
			serving_size=15,
			serving_unit="ml",
			grams_per_ml=0.91,
		)
		food_repo.create(obj_in=olive_oil)

		recipe = service.create_recipe(
			RecipeCreate(
				name="Chicken Salad",
				servings=2,
				items=[
					RecipeItemIn(food_id=chicken.id, quantity=150, unit="g"),
					RecipeItemIn(food_id=olive_oil.id, quantity=1, unit="serving"),
				],
			)
		)

		assert recipe.calories > 0
		assert recipe.per_serving["calories"] == round(recipe.calories / 2, 2)
		assert recipe.per_serving["protein_g"] > 0
