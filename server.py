
import tornado.ioloop
import tornado.web

from db_client import DBClient

PORT = 8888

class TasksHandler(tornado.web.RequestHandler):
    def initialize(self, db_client):
        self.db_client = db_client

    def get(self, user_id):
        try:
            tasks = self.db_client.get_tasks_by_user_id(user_id)
        except RuntimeError as ex:
            raise tornado.web.HTTPError(400, reason=str(ex))

        self.write({ "tasks": tasks })

if __name__ == "__main__":
    db_client = DBClient()

    application = tornado.web.Application([
        # URL Mapping
        (r"/tasks/user/([0-9]+)/?", TasksHandler, dict(db_client=db_client)),
    ])

    print "Server started on port", PORT

    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

