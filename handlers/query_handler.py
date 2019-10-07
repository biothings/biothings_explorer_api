from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from biothings_explorer.user_query_dispatcher import MultiEdgeQueryDispatcher
from biothings_explorer.registry import Registry
from networkx.readwrite import json_graph
import json
import ast
from .base import BaseHandler

reg = Registry()


class SingleHopQueryHandler(BaseHandler):
    def get(self):
        input_cls = self.get_query_argument('input_cls', None)
        input_id = self.get_query_argument('input_id', None)
        input_obj = self.get_query_argument('input_obj', None)
        output_cls = self.get_query_argument('output_cls', None)
        output_id = self.get_query_argument('output_id', None)
        pred = self.get_query_argument('predicate', None)
        if input_obj:
            input_obj = ast.literal_eval(input_obj)
        _id, _value = input_id.split(':', 1)
        _id = "bts:" + _id
        print(input_cls, _id, input_obj, output_cls, output_id, pred, _value)
        seqd = SingleEdgeQueryDispatcher(input_cls=input_cls,
                                         input_id=_id,
                                         input_obj=input_obj,
                                         output_cls=output_cls,
                                         output_id=output_id,
                                         pred=pred,
                                         values=_value,
                                         registry=reg)
        seqd.query()
        res = json_graph.node_link_data(seqd.G)
        if res:
            self.set_status(200)
            self.write(json.dumps(res))
            self.finish()
            return


class MultiHopQueryHandler(BaseHandler):
    def get(self):
        input_obj = self.get_query_argument('input_obj')
        edges = self.get_query_argument('edges')
        if input_obj:
            input_obj = ast.literal_eval(input_obj)
        if edges:
            edges = ast.literal_eval(edges)
        meqd = MultiEdgeQueryDispatcher(input_obj=input_obj,
                                        edges=edges,
                                        registry=reg)
        meqd.query()
        res = json_graph.node_link_data(meqd.G)
        if res:
            self.set_status(200)
            self.write(json.dumps(res))
            self.finish()
            return
