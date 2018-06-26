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

query task($taskId: Int!, $withProject: Boolean = true) {
  task(id: $taskId) {
    ...taskFragment
    project @include(if: $withProject) {
      id
      name
    }
  }
  anotherTask: task(id: 2) {
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