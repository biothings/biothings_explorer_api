import json
import ast
import pandas as pd
import tornado.escape
from urllib.parse import parse_qs
from .base import BaseHandler
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import FindConnection

reg = Registry()

class ConnectHandler(BaseHandler):
    def get(self):
        input_obj = self.get_query_argument('input_obj')
        output_obj = self.get_query_argument('output_obj')
        print("executing connect query: ", self.request.uri)
        intermediate_nodes = self.get_query_argument('intermediate_nodes')
        if type(input_obj) == str:
            input_obj = tornado.escape.json_decode(input_obj)
        if type(output_obj) == str:
            output_obj = tornado.escape.json_decode(output_obj)
        if type(intermediate_nodes) == str:
            intermediate_nodes = ast.literal_eval(intermediate_nodes)
        fc = FindConnection(input_obj=input_obj,
                            output_obj=output_obj,
                            intermediate_nodes=intermediate_nodes,
                            registry=reg)
        fc.connect()
        df = fc.display_table_view()
        if df.empty:
            res = []
        else:
            df = df[['input', 'pred1', 'pred1_api', 'node1_name', 'node1_type', 'pred2', 'pred2_api', 'output_name']]
            df.drop_duplicates(inplace=True)
            res = df.to_dict('records')
        if res:
            self.set_status(200)
            self.write(tornado.escape.json_encode({'data': res, 'log': fc.fc.log}))
            self.finish()
            return
        else:
            self.set_status(404)
            self.write(json.dumps({'error': "Unable to find any connection"}))
            self.finish()
            return
