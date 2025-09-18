from __future__ import annotations

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Food(Base):
	__tablename__ = "foods"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(120), unique=True, index=True)

	# Nutrition values are per serving
	calories: Mapped[int] = mapped_column()
	protein_g: Mapped[float] = mapped_column()
	carbs_g: Mapped[float] = mapped_column()
	fat_g: Mapped[float] = mapped_column()
	fiber_g: Mapped[float] = mapped_column(default=0.0)
	sugar_g: Mapped[float] = mapped_column(default=0.0)
	saturated_fat_g: Mapped[float] = mapped_column(default=0.0)
	sodium_mg: Mapped[float] = mapped_column(default=0.0)
	potassium_mg: Mapped[float] = mapped_column(default=0.0)
	cholesterol_mg: Mapped[float] = mapped_column(default=0.0)
	additional_nutrients: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)

	# Serving metadata
	serving_size: Mapped[float] = mapped_column(default=1.0)
	serving_unit: Mapped[str] = mapped_column(String(16), default="serving")  # serving|g|ml|piece
	grams_per_ml: Mapped[float | None] = mapped_column(default=None)  # density to convert ml<->g
