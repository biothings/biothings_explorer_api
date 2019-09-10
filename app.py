import tornado.httpserver
import tornado.ioloop
import tornado.web

from handlers.hint_handler import HintHandler
from handlers.schema_handler import SchemaHandler
from handlers.connect_handler import ConnectHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/v1/hint", HintHandler),
            (r"/api/v1/find_edge", SchemaHandler),
            (r"/api/v1/connect", ConnectHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


def main():
    app = Application()
    app.listen(8855)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
