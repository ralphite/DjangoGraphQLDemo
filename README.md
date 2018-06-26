# Django GraphQL CRUD Demo

---

```sh
pip3 install virtualenv
source ./virtualenv/bin/activate
pip3 install -r djserver/requirements.txt
python3 manage.py migrate
python3 manage.py loaddata tasks
python3 manage.py runserver
open http://localhost:8000/graphql
```

```json

query task($taskId: Int) {
  task(id: $taskId) {
    id
    name
    completed
    project {
      id
      name
    }
  }
}

{
  "taskId": 1
}

```