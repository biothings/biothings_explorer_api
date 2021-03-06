from biothings_explorer.metadata import Metadata
from biothings_explorer.config import metadata
from biothings_explorer.registry import Registry
import json
from .base import BaseHandler

md = Metadata()
reg = Registry()


class SemanticTypesHandler(BaseHandler):
    """Return all semantic types used in bt explorer"""
    def get(self):
        result = md.list_all_semantic_types()
        self.set_status(200)
        self.write(json.dumps(result))
        self.finish()


class PredicatesHandler(BaseHandler):
    """Return all predicates using in bt explorer"""
    def get(self):
        result = md.list_all_predicates()
        self.set_status(200)
        self.write(json.dumps(result))
        self.finish()


class AssociationsHandler(BaseHandler):
    """Return all associations using in bt explorer"""
    def get(self):
        result = md.list_all_associations()
        self.set_status(200)
        self.write(json.dumps(result))
        self.finish()


class IDTypesHandler(BaseHandler):
    """Return all id types using in bt explorer"""
    def get(self):
        result = md.list_all_id_types()
        self.set_status(200)
        self.write(json.dumps(result))
        self.finish()


class EdgeFilterHandler(BaseHandler):
    """Return all associations based on input/output/predicate"""
    def get(self):
        input_cls = self.get_query_argument('input_cls', None)
        output_cls = self.get_query_argument('output_cls', None)
        pred = self.get_query_argument('pred', None)
        result = md.registry.filter_edges(input_cls=input_cls,
                                          edge_label=pred,
                                          output_cls=output_cls)
        associations = set()
        for _res in result:
            _item = _res['input_type'] + '|' + _res['label'] + '|' + _res['output_type']
            associations.add(_item)
        final_res = []
        for _assoc in associations:
            s, p, o = _assoc.split('|')
            final_res.append((s, p, o))
        self.set_status(200)
        self.write(json.dumps(final_res))
        self.finish()

class DetailedAssociationsHandler(BaseHandler):
    def get(self):
        res = {'associations': []}
        for sbj_id,  obj_id, assoc in reg.G.edges(data=True):
            tmp = {
                'subject': {
                    'identifier': sbj_id,
                    'semantic_type': assoc['input_type']
                },
                'object': {
                    'identifier': obj_id,
                    'semantic_type': assoc['output_type']
                },
                'predicate': {
                    'source': assoc['operation'].get('source'),
                    'label': assoc['label']
                },
                'api': {
                    'name': assoc['operation']["api_name"],
                    'smartapi': {
                        'url': "http://smart-api.info/registry?q=" + assoc['operation']["api_name"],
                    }
                }
            }
            res['associations'].append(tmp)
        self.set_status(200)
        self.write(json.dumps(res))
        self.finish()
