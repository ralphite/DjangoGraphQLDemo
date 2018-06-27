# Django GraphQL CRUD Demo


```bash
pip3 install virtualenv
source ./virtualenv/bin/activate
pip3 install -r djserver/requirements.txt
python3 manage.py migrate
python3 manage.py loaddata tasks
python3 manage.py runserver
open http://localhost:8000/graphql
```

```graphql

query ReadTask($taskId: Int!, $withProject: Boolean = true) {
  task(id: $taskId) {
    ...taskFragment
    project @include(if: $withProject) {
      id
      name
    }
  }
  anotherTask: task(id: 2) {
    __typename
    ...taskFragment
  }
}

fragment taskFragment on TaskType {
  name
  completed
}

{
  "taskId": 1
}

```

```graphql

mutation {
  createProject(name: "A new project") {
		status
    message
    project {
      id
      name
    }
  }

  updateTask(taskId: 1, projectId: 2) {
    status
    message
    task {
      id
      name
      project {
        id
        name
      }
    }
  }

  deleteTask(taskId: 6) {
    status
    message
  }
}

```