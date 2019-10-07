import json
import ast
from .base import BaseHandler
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import Connect
from biothings_explorer.networkx_helper import networkx_json_to_visjs

reg = Registry()


class ConnectHandler(BaseHandler):
    def get(self):
        _input = self.get_query_argument('input')
        _output = self.get_query_argument('output')
        steps = self.get_query_argument('steps', 2)
        _format = self.get_query_argument('format', None)
        if type(_input) == str:
            _input = ast.literal_eval(_input)
        if type(_output) == str:
            _output = ast.literal_eval(_output)
        ctc = Connect(input_obj=_input,
                      output_obj=_output,
                      max_steps=steps,
                      registry=reg)
        ctc.connect()
        res = ctc.to_json()
        if _format == "visjs":
            res = networkx_json_to_visjs(res)
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
