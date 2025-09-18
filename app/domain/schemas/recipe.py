from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class RecipeItemIn(BaseModel):
	food_id: int = Field(ge=1)
	quantity: float = Field(gt=0)
	unit: str = Field(pattern=r"^(serving|g|ml|piece)$", default="serving")


class RecipeBase(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	name: str = Field(min_length=1, max_length=160)
	additional_nutrients: Dict[str, float] = Field(default_factory=dict)
	servings: float = Field(gt=0, default=1.0)
	serving_unit: str = Field(pattern=r"^(serving|g|ml|piece)$", default="serving")


class RecipeCreate(RecipeBase):
	items: List[RecipeItemIn] = Field(default_factory=list)


class RecipeUpdate(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	name: Optional[str] = Field(default=None, min_length=1, max_length=160)
	additional_nutrients: Optional[Dict[str, float]] = None
	servings: Optional[float] = Field(default=None, gt=0)
	serving_unit: Optional[str] = Field(default=None, pattern=r"^(serving|g|ml|piece)$")


class RecipeItemOut(BaseModel):
	id: int
	food_id: int
	quantity: float
	unit: str


class RecipeOut(RecipeBase):
	id: int
	# Whole recipe totals
	calories: int
	protein_g: float
	carbs_g: float
	fat_g: float
	fiber_g: float
	sugar_g: float
	saturated_fat_g: float
	sodium_mg: float
	potassium_mg: float
	cholesterol_mg: float
	# Derived per serving (server-side convenience)
	per_serving: Dict[str, float] = Field(default_factory=dict)
	items: List[RecipeItemOut] = Field(default_factory=list)
