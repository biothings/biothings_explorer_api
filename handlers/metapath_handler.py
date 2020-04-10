import json
from itertools import groupby
from collections import defaultdict
from operator import itemgetter
from .base import BaseHandler
from biothings_explorer.registry import Registry

reg = Registry()

class MetaPathHandler(BaseHandler):
    def get(self):
        input_cls = self.get_query_argument('input_cls')
        output_cls = self.get_query_argument('output_cls')
        result = []
        tmp = defaultdict(list)
        grouper = itemgetter("output_type")
        input_connects = reg.filter_edges(input_cls=input_cls)
        if input_connects:    
            for group, _ in groupby(sorted(input_connects, key=grouper), grouper):
                tmp[group].append([input_cls, group])
                if group == output_cls:
                    result.append([input_cls, output_cls])
        for intermediate_node, tmp_paths in tmp.items():
            intermediate_connects = reg.filter_edges(input_cls=intermediate_node,
                                                     output_cls=output_cls)
            if not intermediate_connects:
                continue
            for tmp_path in tmp_paths:
                tmp_path += [output_cls]
                result.append(tmp_path)
        if result:
            result = [','.join(item) for item in result]
            self.set_status(200)
            self.write(json.dumps({'edges': result,
                                   'source': input_cls,
                                   'target': output_cls}))
            self.finish()
            return
        else:
            self.set_status(404)
            self.write(json.dumps({'error': "Unable to find any edges"}))
            self.finish()
            return

