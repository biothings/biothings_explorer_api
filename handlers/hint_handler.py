from biothings_explorer.hint import Hint
import json
from .base import BaseHandler

ht = Hint()


class HintHandler(BaseHandler):
    def get(self):
        _input = self.get_query_argument('q', None)
        if _input:
            try:
                result = ht.query(_input)
                self.set_status(200)
                self.write(json.dumps(result))
                self.finish()
            except:
                self.set_status(400)
                self.write(json.dumps({'error': 'No input is found'}))
        else:
            self.set_status(400)
            self.write(json.dumps({'error': 'No input is found'}))
