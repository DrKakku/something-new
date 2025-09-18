from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Food


class FoodRepository:
	def __init__(self, session: Session) -> None:
		self._session = session

	def create(self, *, obj_in: Food) -> Food:
		self._session.add(obj_in)
		self._session.flush()
		return obj_in

	def get_by_id(self, *, food_id: int) -> Optional[Food]:
		return self._session.get(Food, food_id)

	def get_by_name(self, *, name: str) -> Optional[Food]:
		stmt = select(Food).where(Food.name == name)
		return self._session.scalar(stmt)

	def list_all(self, *, limit: int = 100, offset: int = 0) -> Iterable[Food]:
		stmt = select(Food).offset(offset).limit(limit)
		return self._session.scalars(stmt)

	def delete(self, *, food_id: int) -> bool:
		food = self.get_by_id(food_id=food_id)
		if food is None:
			return False
		self._session.delete(food)
		return True
