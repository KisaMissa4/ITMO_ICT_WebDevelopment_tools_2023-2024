# Документация API для работы с проектами и пользователями

Этот API предоставляет функционал для управления проектами, задачами и пользователями в системе. Все эндпоинты работают через
асинхронные запросы и используют `FastAPI`, `SQLModel` и асинхронные сессии для работы с базой данных.

## Общие принципы API

- Эндпоинты организованы в два основных префикса: `/projects` и `/client`.
- Пользователи могут создавать проекты, присоединяться к ним, управлять задачами и менять информацию о себе.
- Для работы с API используется аутентификация через JWT, которая обеспечивается за счет зависимости `get_user`.

---

## Эндпоинты для работы с проектами

### `GET /projects`

Возвращает список всех проектов. Если передан параметр `is_active`, фильтрует проекты по их активности.

**Параметры:**

- `is_active` (опционально, `bool`) — фильтр по активности проекта.

**Пример запроса:**

```http
GET /projects?is_active=true
```

**Пример ответа:**

```json
[
  {
    "id": 1,
    "title": "Project 1",
    "description": "Description of project 1",
    "is_active": true,
    "start_date": "2023-05-15T10:00:00Z",
    "end_date": null
  },
  {
    "id": 2,
    "title": "Project 2",
    "description": "Description of project 2",
    "is_active": false,
    "start_date": "2023-01-01T12:00:00Z",
    "end_date": "2023-07-01T12:00:00Z"
  }
]
```

---

### `POST /projects/{project_id}/join`

Позволяет пользователю присоединиться к проекту. Пользователь и проект передаются через зависимости.

**Тело запроса:**

```json
{
  "role": "Developer"
}
```

**Пример ответа:**

```json
"OK"
```

---

## Эндпоинты для работы с пользователями и их проектами

### `GET /client/me`

Возвращает информацию о текущем пользователе, а также проекты, которые он создал, и его навыки.

**Пример ответа:**

```json
{
  "id": 1,
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "created_projects": [
    {
      "id": 1,
      "title": "Project 1",
      "description": "Description of project 1",
      "is_active": true,
      "start_date": "2023-05-15T10:00:00Z",
      "end_date": null
    }
  ],
  "skills": [
    {
      "name": "Python",
      "description": "Programming language",
      "level": 3
    }
  ]
}
```

---

### `PUT /client/me`

Позволяет обновить информацию о текущем пользователе.

**Тело запроса:**

```json
{
  "first_name": "Jane",
  "last_name": "Doe"
}
```

**Пример ответа:**

```json
{
  "id": 1,
  "username": "john_doe",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

---

### `GET /client/me/createdProjects`

Возвращает список проектов, созданных текущим пользователем.

**Пример ответа:**

```json
[
  {
    "id": 1,
    "title": "Project 1",
    "description": "Description of project 1",
    "is_active": true,
    "start_date": "2023-05-15T10:00:00Z",
    "end_date": null
  }
]
```

---

### `POST /client/me/createdProjects`

Создает новый проект от имени текущего пользователя.

**Тело запроса:**

```json
{
  "title": "New Project",
  "description": "Description of the new project",
  "is_active": true,
  "start_date": "2023-09-15T10:00:00Z"
}
```

**Пример ответа:**

```json
{
  "id": 3,
  "title": "New Project",
  "description": "Description of the new project",
  "is_active": true,
  "start_date": "2023-09-15T10:00:00Z",
  "end_date": null
}
```

---

### `GET /client/me/createdProjects/{project_id}/members`

Возвращает список участников проекта, созданного текущим пользователем, вместе с их ролями.

**Пример ответа:**

```json
[
  {
    "id": 2,
    "username": "alice",
    "role": "Developer"
  },
  {
    "id": 3,
    "username": "bob",
    "role": "Tester"
  }
]
```

---

### `GET /client/me/createdProjects/{project_id}/tasks`

Возвращает список задач для проекта, созданного текущим пользователем.

**Пример ответа:**

```json
[
  {
    "id": 1,
    "name": "Setup environment",
    "description": "Set up the development environment",
    "status": "New",
    "due_date": "2023-09-30T12:00:00Z"
  }
]
```

---

### `POST /client/me/createdProjects/{project_id}/tasks`

Создает новую задачу для проекта, созданного текущим пользователем.

**Тело запроса:**

```json
{
  "name": "New task",
  "description": "Description of the new task",
  "status": "New",
  "due_date": "2023-10-01T12:00:00Z"
}
```

**Пример ответа:**

```json
{
  "id": 2,
  "name": "New task",
  "description": "Description of the new task",
  "status": "New",
  "due_date": "2023-10-01T12:00:00Z"
}
```

---

### `PUT /client/me/createdProjects/{project_id}/tasks/{task_id}`

Обновляет задачу в проекте, созданном текущим пользователем.

**Тело запроса:**

```json
{
  "name": "Updated task name",
  "description": "Updated task description",
  "status": "In progress"
}
```

**Пример ответа:**

```json
{
  "id": 1,
  "name": "Updated task name",
  "description": "Updated task description",
  "status": "In progress",
  "due_date": "2023-09-30T12:00:00Z"
}
```

---

### `DELETE /client/me/createdProjects/{project_id}/tasks/{task_id}`

Удаляет задачу из проекта, созданного текущим пользователем.

**Пример ответа:**

```json
"OK"
```

---

### `GET /client/me/memberProjects`

Возвращает список проектов, в которых текущий пользователь является участником (но не создателем).

**Пример ответа:**

```json
[
  {
    "id": 2,
    "title": "Project 2",
    "description": "Description of project 2",
    "is_active": true,
    "start_date": "2023-07-01T10:00:00Z"
  }
]
```

---

### `GET /client/me/memberProjects/{project_id}/tasks`

Возвращает список задач, назначенных текущему пользователю в проекте, в котором он является участником.

**Пример ответа:**

```json
[
  {
    "id": 1,
    "name": "Task 1",
    "description": "Description of task 1",
    "status": "In progress",
    "due_date": "2023-09-30T12:00:00Z"
  }
]
```

---

### `PUT /client/me/memberProjects/{project_id}/tasks/{task_id}`

Обновляет статус задачи, назначенной текущему пользователю в проекте, в котором он является участником.

**Тело запроса:**

```json
{
  "status": "Completed"
}
```

**Пример ответа:**

```json
{
  "id": 1,
  "name": "Task 1",
  "description": "Description of task 1",
  "status": "Completed",
  "due_date": "2023-09-30T12:00:00Z"
}
```

---

## Заключение

Этот API предоставляет полный набор возможностей для управления проектами, задачами и пользователями, включая создание
проектов, присоединение к ним, управление задачами и обновление информации о пользователе. Все операции производятся
асинхронно, что повышает производительность системы при большом количестве запросов.
