import unittest
from fastapi.testclient import TestClient
from fastapi_tortoise_app.main import app

class TestTaskAPI(unittest.TestCase):

    def test_create_task(self):
        with TestClient(app) as client:
            response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test task."})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["title"], "Test Task")
            self.assertEqual(data["description"], "This is a test task.")
            self.assertFalse(data["is_completed"])
            self.task_id = data["id"]

    def test_read_task(self):
        with TestClient(app) as client:
            response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test task."})
            task_id = response.json()["id"]
            response = client.get(f"/tasks/{task_id}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["title"], "Test Task")
            self.assertEqual(data["description"], "This is a test task.")
            self.assertFalse(data["is_completed"])

    def test_read_tasks(self):
        with TestClient(app) as client:
            client.post("/tasks", json={"title": "Test Task 1", "description": "This is test task 1.", "is_completed": True})
            client.post("/tasks", json={"title": "Test Task 2", "description": "This is test task 2.", "is_completed": False})

            response = client.get("/tasks")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(len(data), 2)

            response = client.get("/tasks?is_completed=true")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(len(data), 1)
            self.assertTrue(data[0]["is_completed"])

    def test_update_task(self):
        with TestClient(app) as client:
            response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test task."})
            task_id = response.json()["id"]
            response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated description."})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["title"], "Updated Task")
            self.assertEqual(data["description"], "Updated description.")
            self.assertFalse(data["is_completed"])

    def test_delete_task(self):
        with TestClient(app) as client:
            response = client.post("/tasks", json={"title": "Test Task", "description": "This is a test task."})
            task_id = response.json()["id"]
            response = client.delete(f"/tasks/{task_id}")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["deleted"], 1)

            response = client.get(f"/tasks/{task_id}")
            self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
