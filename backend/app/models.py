# データベースのテーブル定義

from sqlalchemy import Column, Integer, String
from .database import Base # 先ほど作成したdatabase.pyからBaseをインポート

# 'todos' テーブルを表現するTodoモデルクラスを定義します
class Todo(Base):
    __tablename__ = "todos" # データベース上でのテーブル名

    # カラムの定義
    id = Column(Integer, primary_key=True, index=True) # 主キーとなるID
    content = Column(String, index=True) # Todoのタイトル
