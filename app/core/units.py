from __future__ import annotations

from typing import Literal

Unit = Literal["serving", "g", "ml", "piece"]


def to_serving_multiplier(
	*, quantity: float, unit: Unit, food_serving_size: float, food_serving_unit: Unit, grams_per_ml: float | None
) -> float:
	"""
	Return multiplier of a food's base serving represented by the provided quantity/unit.
	- If unit == food_serving_unit: multiplier = quantity / food_serving_size
	- If converting g<->ml uses grams_per_ml (density), if missing and needed, fall back to 1:1.
	- "piece" behaves like a serving unless food_serving_unit is also piece.
	"""
	if unit == food_serving_unit:
		return quantity / food_serving_size

	# Normalize to grams when possible
	if unit == "g" and food_serving_unit == "ml":
		density = grams_per_ml or 1.0
		ml = quantity / (density if density > 0 else 1.0)
		return ml / food_serving_size
	if unit == "ml" and food_serving_unit == "g":
		density = grams_per_ml or 1.0
		grams = quantity * (density if density > 0 else 1.0)
		return grams / food_serving_size

	# piece or serving conversions: treat as serving-based measure
	if unit == "piece" and food_serving_unit == "serving":
		return quantity / food_serving_size
	if unit == "serving" and food_serving_unit == "piece":
		return quantity / food_serving_size

	# Fallback naive ratio when no specific mapping
	return quantity / food_serving_size
