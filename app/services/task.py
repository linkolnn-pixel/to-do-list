from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    """Ключевые операции с задачами, включая бизнес-логику, валидацию и прочее"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task = self.repository.create(title=task_create.title)
        self.db.commit()
        self.db.refresh(task)
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task = self.repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.completed is not None:
            task.completed = task_update.completed
        self.db.commit()
        self.db.refresh(task)
        return TaskSchema.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        task = self.repository.get_by_id(task_id=task_id)
        if not task:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        self.repository.delete(task)
        self.db.commit()
