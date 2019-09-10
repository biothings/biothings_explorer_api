import json
from .base import BaseHandler
from biothings_explorer.registry import Registry

reg = Registry()


class SchemaHandler(BaseHandler):
    def get(self):
        input_cls = self.get_query_argument('input_cls', None)
        output_cls = self.get_query_argument('output_cls', None)
        edges = set()
        if input_cls:
            for (u, v, e) in reg.G.edges(data=True):
                if e['input_type'] == input_cls:
                    if e['label']:
                        edges.add(e['label'][4:])
        if output_cls:
            for (u, v, e) in reg.G.edges(data=True):
                if e['output_type'] == output_cls:
                    if e['label']:
                        edges.add(e['label'][4:])
        if edges:
            self.set_status(200)
            self.write(json.dumps({'edges': list(edges)}))
            self.finish()
            return
        else:
            self.set_status(404)
            self.write(json.dumps({'error': "Unable to find any edges"}))
            self.finish()
            return

