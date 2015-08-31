
Requirements:
* Python 2 (tested on Python 2.7.6)
* virtualenv (https://virtualenv.pypa.io/en/latest/installation.html)

Setup:
```
> ./bootstrap.sh
```

Running:
```
> source venv/bin/activate # Just once
> python server.py
```

URL Mapping:
```
http://localhost:8888/tasks/user/[user_id]
GET: Returns list of all tasks for a user

POST: Create new task for a user.
Body = JSON of task with a due_date and description
```
```
http://localhost:8888/tasks/user/[user_id]?incomplete-only=true
GET: Returns list of all incomplete tasks for a user
```
```
http://localhost:8888/tasks/[task_id]
PUT: Updates a task with specified fields
Body = JSON of task with fields to update (description, due_date, is_complete)
```

Examples:
```
>./curl-scripts/get_tasks.sh # To get tasks for a user
>./curl-scripts/get_incomplete_tasks.sh # To get incomplete tasks for a user
>./curl-scripts/create_new_task.sh # Creating a new task for a user
>./curl-scripts/update_task_complete.sh # Updating a new task to be completed
```

Other Info:
* Backend is sqlite3
* Ran on OS X Yosemite, but everything should work in linux
* Please let me know if you have any questions!

