# FastAPI Task CRUD API

This project is a simple CRUD (Create, Read, Update, Delete) API for managing tasks using FastAPI and Tortoise ORM with an in-memory SQLite database. It allows users to create, retrieve, update, and delete tasks, as well as filter tasks based on their completion status.

## Features

- Create a new task
- Retrieve a task by ID
- Retrieve all tasks with optional filtering by completion status
- Update an existing task
- Delete a task

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Tortoise ORM**: An easy-to-use asyncio ORM inspired by Django.
- **SQLite**: A lightweight, in-memory database for development and testing.
- **Poetry**: Dependency management and packaging tool for Python.

## Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your machine.

### Clone the Repository

```bash
git clone git@github.com:akailash/fastapi_tortoise_app.git
cd fastapi_tortoise_app
```

### Install Dependencies with Poetry

You can install the required packages using Poetry:

```bash
poetry install
```

## Running the Application

To run the application, use the following command:

```bash
poetry run uvicorn fastapi_tortoise_app.main:app --reload
```

This starts the FastAPI server at `http://127.0.0.1:8000`.

## API Endpoints

### Create a Task

- **Endpoint**: `POST /tasks`
- **Request Body**:
  ```json
  {
    "title": "Task Title",
    "description": "Task Description"
  }
  ```

### Read a Task

- **Endpoint**: `GET /tasks/{task_id}`
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "is_completed": false,
    "created_at": "2023-01-01T00:00:00Z"
  }
  ```

### Read All Tasks

- **Endpoint**: `GET /tasks`
- **Query Parameters**: `is_completed` (optional)
- **Response**: A list of tasks.

### Update a Task

- **Endpoint**: `PUT /tasks/{task_id}`
- **Request Body**:
  ```json
  {
    "title": "Updated Task Title",
    "description": "Updated Description"
  }
  ```

### Delete a Task

- **Endpoint**: `DELETE /tasks/{task_id}`
- **Response**:
  ```json
  {
    "deleted": 1
  }
  ```

## Running Tests

To run the tests for the API, use the following command:

```bash
poetry run python -m unittest tests/test_main.py
```

This will execute all the test cases defined in `test_main.py` to ensure the API behaves as expected.
