from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound, CategoryService


def test_list_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    # Имитируем, что метод get_all репозитория вернет эти задачи
    category_repository_mock.get_all.return_value = [
        CategoryORM(id="category-1", name="Pytest"),
        CategoryORM(id="category-2", name="Дом"),
    ]

    result = category_service.list_categories()

    assert result == [
        CategorySchema(id="category-1", name="Pytest"),
        CategorySchema(id="category-2", name="Дом"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    created_category = CategoryORM(id="category-1", name="Новая категория")
    category_repository_mock.create.return_value = created_category
    result = category_service.create_category(
        CategoryCreateSchema(name="Новая категория")
    )

    category_repository_mock.create.assert_called_once_with(name="Новая категория")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая категория",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Обновить наименование"),  # payload
            "Обновить наименование",  # expected_name
        ),
        pytest.param(
            CategoryUpdateSchema(),  # payload
            "Старая категория",  # expected_name
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
) -> None:
    category = CategoryORM(id="category-1", name="Старая категория")
    category_repository_mock.get_by_id.return_value = category

    result = category_service.update_category("category-1", payload)

    category_repository_mock.get_by_id.assert_called_once_with(category_id="category-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_category_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):  # Должна произойти указанная ошибка
        category_service.update_category(
            "missing-category", CategoryUpdateSchema(name="Неважно")
        )

    db_mock.commit.assert_not_called()
