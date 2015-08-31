
import json

import tornado.ioloop
import tornado.web

from db_client import DBClient

PORT = 8888

def request_as_json(request):
    if request.headers["Content-Type"] != "application/json":
        raise tornado.web.HTTPError(400, reason="Content-Type must be application/json")
    return json.loads(request.body)

def validate_attribute(check_attribute, attributes):
    if check_attribute not in attributes:
        raise tornado.web.HTTPError(400,
                reason="{0} not in attributes: {1}".format(check_attribute,
                                                           attributes))

class TasksUserHandler(tornado.web.RequestHandler):
    def initialize(self, db_client):
        self.db_client = db_client

    def get(self, user_id):
        try:
            tasks = self.db_client.get_tasks_by_user_id(user_id)
        except RuntimeError as ex:
            raise tornado.web.HTTPError(400, reason=str(ex))
        except Exception as ex:
            raise tornado.web.HTTPError(500, reason=str(ex))

        self.write({ "tasks": tasks })

    def post(self, user_id):
        task_create = request_as_json(self.request)

        validate_attribute("task", task_create)

        task = task_create["task"]
        validate_attribute("description", task)
        validate_attribute("due_date", task)

        try:
            create_task = self.db_client.create_task(user_id, task)
        except RuntimeError as ex:
            raise tornado.web.HTTPError(400, reason=str(ex))


class TasksHandler(tornado.web.RequestHandler):
    def initialize(self, db_client):
        self.db_client = db_client

    def put(self, task_id):
        task_update = request_as_json(self.request)

        validate_attribute("task", task_update)
        task = task_update["task"]

        try:
            self.db_client.update_task(task_id, task)
        except RuntimeError as ex:
            raise tornado.web.HTTPError(400, reason=str(ex))

if __name__ == "__main__":
    db_client = DBClient()

    application = tornado.web.Application([
        # URL Mapping
        (r"/tasks/user/([0-9]+)/?", TasksUserHandler, dict(db_client=db_client)),
        (r"/tasks/([0-9]+)/?", TasksHandler, dict(db_client=db_client)),
    ])

    print "Server started on port", PORT

    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

