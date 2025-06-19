import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# アプリケーションのメインファイルと、依存性注入される関数をインポート
from app.main import app
from app.database import get_db, Base

# --- テスト用のデータベース設定 ---
# 1. テスト用のインメモリSQLiteデータベースURLを定義
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 2. テスト用のデータベースエンジンを作成
#    - connect_args: FastAPIのドキュメント推奨設定
#    - poolclass: テスト実行時に単一の接続を維持するための設定
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# 3. テスト用のデータベースセッションを作成するためのクラス
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- 依存性のオーバーライド ---
def override_get_db():
    """
    テスト実行時に、本来のget_dbの代わりに使用される関数。
    テスト用のデータベースセッションを提供する。
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 4. FastAPIアプリの依存性を、テスト用のものに上書き
app.dependency_overrides[get_db] = override_get_db


# --- pytestフィクスチャの定義 ---
@pytest.fixture()
def client():
    """
    各テストケースに、クリーンなデータベースとTestClientを提供するフィクスチャ。
    このフィクスチャは、テスト関数が実行されるたびに呼び出される。
    """
    # 5. テストが始まる前に、全てのテーブルを作成する（クリーンな状態）
    Base.metadata.create_all(bind=engine)
    
    # 6. TestClientを生成してテストに提供
    yield TestClient(app)
    
    # 7. テストが終わった後に、全てのテーブルを削除する（後片付け）
    Base.metadata.drop_all(bind=engine)

