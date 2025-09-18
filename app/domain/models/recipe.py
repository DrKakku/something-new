from __future__ import annotations

from typing import List

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Recipe(Base):
	__tablename__ = "recipes"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(160), unique=True, index=True)

	# Aggregated totals (whole recipe)
	calories: Mapped[int] = mapped_column(default=0)
	protein_g: Mapped[float] = mapped_column(default=0.0)
	carbs_g: Mapped[float] = mapped_column(default=0.0)
	fat_g: Mapped[float] = mapped_column(default=0.0)
	fiber_g: Mapped[float] = mapped_column(default=0.0)
	sugar_g: Mapped[float] = mapped_column(default=0.0)
	saturated_fat_g: Mapped[float] = mapped_column(default=0.0)
	sodium_mg: Mapped[float] = mapped_column(default=0.0)
	potassium_mg: Mapped[float] = mapped_column(default=0.0)
	cholesterol_mg: Mapped[float] = mapped_column(default=0.0)
	additional_nutrients: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)

	# Serving metadata for recipe
	servings: Mapped[float] = mapped_column(default=1.0)
	serving_unit: Mapped[str] = mapped_column(String(16), default="serving")

	items: Mapped[List["RecipeItem"]] = relationship(
		back_populates="recipe", cascade="all, delete-orphan"
	)


class RecipeItem(Base):
	__tablename__ = "recipe_items"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True)
	food_id: Mapped[int] = mapped_column(ForeignKey("foods.id", ondelete="RESTRICT"), index=True)
	quantity: Mapped[float] = mapped_column(default=1.0)  # number of food servings by default
	unit: Mapped[str] = mapped_column(String(16), default="serving")  # serving|g|ml|piece
