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

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic_core import ErrorDetails
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder

# カスタムエラーメッセージ
CUSTOM_MESSAGES = {
    "string_type": "{input}は必須項目です。",
    "string_too_long": "{input}は{max_length}文字以下で入力してください。",
    "string_too_short": "{input}は{min_length}文字以上入力してください。",
}

sys.dont_write_bytecode = True
# データベーステーブルを作成
# (もしテーブルが既に存在していても、何もしない)
models.Base.metadata.create_all(bind=engine)

def convert_errors(
    e: ValidationError,
    messages: dict[str, str],
) -> list[ErrorDetails]:
    """バリデーションエラーメッセージをカスタマイズ"""
    new_errors: list[ErrorDetails] = []

    for error in e.errors():
        message = messages.get(error["type"])
        if message:
            ctx = error.get("ctx")
            input = error.get("loc")

            error["msg"] = (
                message.format(input=input[1], **ctx)
                if ctx
                else message.format(input=input[1])
            )
        new_errors.append(error)

    return new_errors

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# 例外ハンドラをオーバーライド
@app.exception_handler(RequestValidationError)
def validation_exception_handler(_, e: RequestValidationError):
    # ここでエラーメッセージを日本語に置換
    exc = convert_errors(e=e, messages=CUSTOM_MESSAGES)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc}),
    )

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     """
#     Pydanticのバリデーションエラーを補足し、
#     独自のレスポンス形式に変換するハンドラ。
#     """
#     # エラーの詳細情報を取得
#     # exc.errors() には、どのフィールドでどんなエラーが起きたかの詳細が入っている
#     # ここではシンプルなメッセージに集約する例
#     error_messages = []
#     for error in exc.errors():
#         field = ".".join(str(loc) for loc in error["loc"])
#         message = error["msg"]
#         error_messages.append(f"'{field}': {message}")

#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "message": "入力データが無効です。",
#             "details": error_messages,
#         },
#     )

# async def generic_exception_handler(request: Request, exc: Exception):
#     """
#     予期せぬサーバーエラーを補足し、
#     汎用的な500エラーレスポンスを返すハンドラ。
#     """
#     # 本番環境では、ここでエラーログを記録することが推奨される

#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={
#             "message": "サーバー内部で予期せぬエラーが発生しました。",
#         },
#     )

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
def read_todos(db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
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
@app.delete("/todos/{todo_id}", response_model=schemas.Todo, responses={
    404: {"model": schemas.ErrorResponse, "description": "Todo not found"},
    500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
})
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
