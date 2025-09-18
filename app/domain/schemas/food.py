from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, ConfigDict, Field


class FoodBase(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	name: str = Field(min_length=1, max_length=120)
	calories: int = Field(ge=0)
	protein_g: float = Field(ge=0)
	carbs_g: float = Field(ge=0)
	fat_g: float = Field(ge=0)
	fiber_g: float = Field(ge=0, default=0)
	sugar_g: float = Field(ge=0, default=0)
	saturated_fat_g: float = Field(ge=0, default=0)
	sodium_mg: float = Field(ge=0, default=0)
	potassium_mg: float = Field(ge=0, default=0)
	cholesterol_mg: float = Field(ge=0, default=0)
	additional_nutrients: Dict[str, float] = Field(default_factory=dict)

	serving_size: float = Field(gt=0, default=1.0)
	serving_unit: str = Field(pattern=r"^(serving|g|ml|piece)$", default="serving")
	grams_per_ml: float | None = Field(default=None, gt=0)


class FoodCreate(FoodBase):
	pass


class FoodUpdate(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	name: str | None = Field(default=None, min_length=1, max_length=120)
	calories: int | None = Field(default=None, ge=0)
	protein_g: float | None = Field(default=None, ge=0)
	carbs_g: float | None = Field(default=None, ge=0)
	fat_g: float | None = Field(default=None, ge=0)
	fiber_g: float | None = Field(default=None, ge=0)
	sugar_g: float | None = Field(default=None, ge=0)
	saturated_fat_g: float | None = Field(default=None, ge=0)
	sodium_mg: float | None = Field(default=None, ge=0)
	potassium_mg: float | None = Field(default=None, ge=0)
	cholesterol_mg: float | None = Field(default=None, ge=0)
	additional_nutrients: Dict[str, float] | None = None
	serving_size: float | None = Field(default=None, gt=0)
	serving_unit: str | None = Field(default=None, pattern=r"^(serving|g|ml|piece)$")
	grams_per_ml: float | None = Field(default=None, gt=0)


class FoodOut(FoodBase):
	id: int
