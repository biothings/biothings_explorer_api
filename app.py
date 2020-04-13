import tornado.httpserver
import tornado.ioloop
import tornado.web

from handlers.hint_handler import HintHandler
from handlers.schema_handler import SchemaHandler
from handlers.metadata_handler import *
from handlers.metapath_handler import MetaPathHandler
from handlers.connect_handler import ConnectHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/explorer_api/v1/hint", HintHandler),
            (r"/explorer_api/v1/find_edge", SchemaHandler),
            (r"/explorer_api/v1/find_metapath", MetaPathHandler),
            (r"/explorer_api/v1/semantictypes", SemanticTypesHandler),
            (r"/explorer_api/v1/predicates", PredicatesHandler),
            (r"/explorer_api/v1/associations", AssociationsHandler),
            (r"/explorer_api/v1/idtypes", IDTypesHandler),
            (r"/explorer_api/v1/filter_edges", EdgeFilterHandler),
            (r"/explorer_api/v1/connect", ConnectHandler)
        ]

        tornado.web.Application.__init__(self, handlers)


def main():
    app = Application()
    app.listen(8855)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
