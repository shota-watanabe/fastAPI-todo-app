# APIのメイン処理

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys

# CORS(Cross-Origin Resource Sharing)を許可するためのミドルウェア
from fastapi.middleware.cors import CORSMiddleware

# これまでに作成したモジュールをインポート
from . import crud, models, schemas
from .database import engine, get_db

sys.dont_write_bytecode = True
# データベーステーブルを作成
# (もしテーブルが既に存在していても、何もしない)
models.Base.metadata.create_all(bind=engine)

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# --- CORS設定 ---
# フロントエンド（Next.js）が動作するオリジンからのリクエストを許可する
origins = [
    "http://localhost",
    "http://localhost:3000", # Next.jsの開発サーバー
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # GET, POST, PUT, DELETEなどすべてのメソッドを許可
    allow_headers=["*"], # すべてのヘッダーを許可
)

# --- APIエンドポイントの定義 ---

# [CREATE] 新しいTodoを作成
@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

# [READ] Todoのリストを取得
@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

# [READ] 特定のIDのTodoを1件取得
@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# [UPDATE] 特定のIDのTodoを更新
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo_data=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# [DELETE] 特定のIDのTodoを削除
@app.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
