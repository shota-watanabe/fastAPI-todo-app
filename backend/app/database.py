# データベース設定

import os
# ORMの1つ(No SQL) https://qiita.com/arkuchy/items/75799665acd09520bed2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースファイルのパスを指定
# backendディレクトリ直下に 'sql_app.db' というファイル名でデータベースが作成される
DATABASE_FILE = "sql_app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DATABASE_FILE}"


# SQLAlchemyの「エンジン」を作成します。これはデータベースとの接続を管理します。
# connect_args はSQLiteを使用する場合にのみ必要です。
# これは、複数のスレッドが同じ接続を共有しないようにするための設定です。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# データベースセッションを管理するためのクラスを作成します。
# このセッションを通じて、データベースへのクエリ（問い合わせ）や操作を行います。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデル（データベースのテーブル定義）のベースとなるクラスを作成します。
# 後ほど作成するモデルクラスは、このBaseを継承します。
Base = declarative_base()

# FastAPIのエンドポイント内でデータベースセッションを取得するための依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
