import json
from networkx.readwrite import json_graph
from .base import BaseHandler
from biothings_explorer.registry import Registry
from biothings_explorer.connect import ConnectTwoConcepts

reg = Registry()


class ConnectHandler(BaseHandler):
    def get(self):
        _input = self.get_query_argument('input', None)
        _output = self.get_query_argument('output', None)
        input_cls, input_id, input_v = _input.split('.')
        output_cls, output_id, output_v = _output.split('.')
        # restructure input as a dict
        rest_input = {'type': input_cls,
                      'identifier': 'bts:' + input_id,
                      'values': input_v}
        # restructure output as a dict
        rest_output = {'type': output_cls,
                       'identifier': 'bts:' + output_id,
                       'values': output_v}
        ctc = ConnectTwoConcepts(rest_input, rest_output,
                                 edge1=None, edge2=None,
                                 registry=reg)
        ctc.connect()
        res = json_graph.node_link_data(ctc.G)
        if res:
            self.set_status(200)
            self.write(json.dumps(res))
            self.finish()
            return
        else:
            self.set_status(404)
            self.write(json.dumps({'error': "Unable to find any connection"}))
            self.finish()
            return
