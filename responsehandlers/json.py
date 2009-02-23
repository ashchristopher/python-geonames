import simplejson

from responsehandler import ResponseHandler

class JsonResponseHandler(ResponseHandler):
    """
    Response handler used that puts reponse data into
    a json structure.
    """
    def get_processed_data(self, input):
        return simplejson.loads(input)