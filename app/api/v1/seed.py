from __future__ import annotations

import random
from typing import List

from fastapi import APIRouter, Depends

from app.core.database import get_session
from app.domain.repositories import FoodRepository
from app.domain.schemas import FoodCreate, FoodOut
from app.domain.services import FoodService

router = APIRouter(prefix="/seed", tags=["seed"])


FOOD_SAMPLES: List[FoodCreate] = [
	FoodCreate(name="Apple", calories=95, protein_g=0.5, carbs_g=25, fat_g=0.3, fiber_g=4.4, sugar_g=19),
	FoodCreate(name="Banana", calories=105, protein_g=1.3, carbs_g=27, fat_g=0.4, fiber_g=3.1, sugar_g=14),
	FoodCreate(name="Chicken Breast 100g", calories=165, protein_g=31, carbs_g=0, fat_g=3.6, saturated_fat_g=1.0, sodium_mg=74),
	FoodCreate(name="Brown Rice 100g", calories=111, protein_g=2.6, carbs_g=23, fat_g=0.9, fiber_g=1.8),
	FoodCreate(name="Olive Oil tbsp", calories=119, protein_g=0, carbs_g=0, fat_g=13.5, saturated_fat_g=2.0),
	FoodCreate(name="Broccoli 100g", calories=34, protein_g=2.8, carbs_g=7, fat_g=0.4, fiber_g=2.6, potassium_mg=316),
]


def get_food_service():
	with get_session() as session:
		yield FoodService(FoodRepository(session))


@router.post("/foods", response_model=list[FoodOut])
async def seed_foods(count: int = 6, service: FoodService = Depends(get_food_service)) -> list[FoodOut]:
	out: list[FoodOut] = []
	choices = FOOD_SAMPLES * ((count // len(FOOD_SAMPLES)) + 1)
	random.shuffle(choices)
	for sample in choices[:count]:
		name = sample.name
		try:
			created = service.create_food(data=sample)
			out.append(created)
		except ValueError:
			# duplicate, skip
			continue
	return out
