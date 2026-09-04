from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryNotFound(Exception):
    """Категория не найдена в БД"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = CategoryRepository(db)

    def list_categories(self) -> list[CategorySchema]:
        categories = self.repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category = self.repository.create(name=category_create.name)
        self.db.commit()
        self.db.refresh(category)
        return CategorySchema.model_validate(category)

    def update_category(
        self, category_id: str, category_update: CategoryUpdateSchema
    ) -> CategorySchema:
        category = self.repository.get_by_id(category_id=category_id)
        if not category:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        if category_update.name is not None:
            category.name = category_update.name
        self.db.commit()
        self.db.refresh(category)
        return CategorySchema.model_validate(category)

    def delete_category(self, category_id: str) -> None:
        category = self.repository.get_by_id(category_id=category_id)
        if not category:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        self.repository.delete(category)
        self.db.commit()
