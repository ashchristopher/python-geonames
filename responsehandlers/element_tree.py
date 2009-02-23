from xml.etree import ElementTree

from responsehandler import ResponseHandler

class ElementTreeResponseHandler(ResponseHandler):
    """
    Response handler used that puts reponse data into
    and ElementTree XML structure.
    """
    def get_processed_data(self, input):
        return ElementTree.XML(input)