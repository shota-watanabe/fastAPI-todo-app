def test_read_todos_on_empty_db(client):
    """Todo一覧が返されること"""
    client.post("/todos/", json={"content": "テストタスク1"})
    client.post("/todos/", json={"content": "テストタスク2"})
    response = client.get("/todos/")
    response = client.get("/todos/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "テストタスク1"
    assert data[1]["content"] == "テストタスク2"

def test_create_todo_success(client):
    """Todoの追加ができること"""
    response = client.post("/todos/", json={"content": "テストタスク"})
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "テストタスク"
    assert "id" in data

def test_create_todo_with_invalid_data(client):
    """バリデーションに違反するデータでTodoを作成しようとした際、422エラーが返ること"""
    # contentが空文字
    response = client.post("/todos/", json={"content": ""})
    assert response.status_code == 422

    # contentが11文字以上
    response = client.post("/todos/", json={"content": "a" * 11})
    assert response.status_code == 422
    
    # contentフィールド自体がない
    response = client.post("/todos/", json={})
    assert response.status_code == 422

def test_read_one_todo(client):
    """特定のIDのTodoが正しく読み取れること"""
    response = client.post("/todos/", json={"content": "読み取りテスト"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["content"] == "読み取りテスト"

def test_read_non_existent_todo(client):
    """存在しないIDのTodoを取得しようとした際、404エラーが返ること"""
    response = client.get("/todos/9999")
    assert response.status_code == 404

def test_update_todo(client):
    """Todoの内容が正しく更新できることを"""
    response = client.post("/todos/", json={"content": "更新前タスク"})
    assert response.status_code == 200
    todo_id = response.json()["id"]
    
    updated_content = "更新後タスク"
    response = client.put(f"/todos/{todo_id}", json={"content": updated_content})
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == updated_content
    
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["content"] == updated_content

def test_update_non_existent_todo(client):
    """存在しないIDのTodoを更新しようとした際、404エラーが返ること"""
    response = client.put("/todos/9999", json={"content": "存在しないタスクの更新"})
    assert response.status_code == 404

def test_delete_todo(client):
    """Todoが正しく削除できること"""
    response = client.post("/todos/", json={"content": "削除テスト"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
    
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []

def test_delete_non_existent_todo(client):
    """存在しないIDのTodoを削除しようとした際、404エラーが返ること"""
    response = client.delete("/todos/9999")
    assert response.status_code == 404
