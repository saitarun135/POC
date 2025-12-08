from sqlalchemy import event
from models.todo_model import ToDoModel
from models.user_todo_link_model import UserToDOsLink


@event.listens_for(ToDoModel, "after_insert")
def after_insert(mapper, connection, target):
    """Keep the user-todo link table in sync when a to-do is created."""
    if not target.created_by:
        return

    connection.execute(
        UserToDOsLink.__table__.insert().values(
            todo_id=target.id,
            user_id=target.created_by,
        )
    )

@event.listens_for(ToDoModel, "after_update")
def after_update(mapper, connection, target):
    if target.status != 1:
        return
    
    connection.execute(
        UserToDOsLink.__table__.update().
            where(UserToDOsLink.todo_id == target.id).
            values(status = 1)
    )