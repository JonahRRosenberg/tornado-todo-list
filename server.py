
import tornado.ioloop
import tornado.web

PORT = 8888

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print self.request
        self.write({"testvals": [1, 2, 3]})

if __name__ == "__main__":
    application = tornado.web.Application([
        # URL Mapping
        (r"/tasks", MainHandler),
    ])

    print "Server started on port", PORT

    application.listen(PORT)
    tornado.ioloop.IOLoop.current().start()

