import pytest


def test_create_and_read_todo(client):
    response = client.post("/api/todos", json={"title": "  Plan the sprint  ", "priority": "high"})
    assert response.status_code == 201
    todo = response.json()
    assert todo["title"] == "Plan the sprint"
    assert todo["priority"] == "high"
    assert todo["completed"] is False
    assert client.get(f"/api/todos/{todo['id']}").json() == todo
    assert client.get("/api/todos").json() == [todo]


@pytest.mark.parametrize("payload", [
    {"title": "   "},
    {"title": "x" * 121},
    {"title": "Task", "priority": "urgent"},
    {"title": "Task", "due_date": "2026-02-30"},
])
def test_rejects_invalid_todo_without_saving(client, payload):
    assert client.post("/api/todos", json=payload).status_code == 422
    assert client.get("/api/todos").json() == []


def test_patch_completes_todo_and_preserves_other_fields(client):
    todo = client.post("/api/todos", json={"title": "Write a test", "description": "First scenario"}).json()
    response = client.patch(f"/api/todos/{todo['id']}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["description"] == todo["description"]
    assert response.json()["created_at"] == todo["created_at"]


def test_delete_removes_todo(client):
    todo = client.post("/api/todos", json={"title": "To delete"}).json()
    assert client.delete(f"/api/todos/{todo['id']}").status_code == 204
    assert client.get(f"/api/todos/{todo['id']}").status_code == 404
