# APIでやり取りするデータの型定義
# Pydanticモデルを使って定義し、データのバリデーション（検証）を自動で行う。
# https://qiita.com/Tadataka_Takahashi/items/8b28f49d67d7e1d65d11

from pydantic import BaseModel, StringConstraints, validator
from typing import Annotated, List, Optional
from fastapi import HTTPException

# APIでデータをやり取りする際のベースとなるスキーマ
class TodoBase(BaseModel):
    content: Annotated[str, StringConstraints(min_length=1, max_length=10)]

# Todoを作成する際に受け取るデータのためのスキーマ
class TodoCreate(TodoBase):
    pass # contentのみを受け取る

# Todoを更新する際に受け取るデータのためのスキーマ
class TodoUpdate(BaseModel):
    content: Optional[str] = None # contentは任意（NoneでもOK）

# APIからデータを返す際のスキーマ
class Todo(TodoBase):
    id: int

    # PydanticモデルがORMモデル（SQLAlchemyモデル）と連携できるようにするための設定
    class Config:
        from_attributes = True

# 汎用的なエラーレスポンスのためのスキーマ
class ErrorResponse(BaseModel):
    detail: str