# CRUD操作

from sqlalchemy.orm import Session
from . import models, schemas # 同じディレクトリ内のmodelsとschemasをインポート

# 指定されたIDのTodoを1件取得する
def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

# Todoのリストを取得する（ページネーション対応）
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

# 新しいTodoを作成する
def create_todo(db: Session, todo: schemas.TodoCreate):
    # スキーマからモデルインスタンスを作成
    db_todo = models.Todo(content=todo.content)
    db.add(db_todo) # セッションに追加
    db.commit()      # データベースにコミット（保存）
    db.refresh(db_todo) # 作成されたTodoの情報（IDなど）を更新
    return db_todo

# 指定されたIDのTodoを更新する
def update_todo(db: Session, todo_id: int, todo_data: schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        # todo_dataからNoneでない値のみを取得して更新
        update_data = todo_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        
        db.commit()
        db.refresh(db_todo)
    return db_todo

# 指定されたIDのTodoを削除する
def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
