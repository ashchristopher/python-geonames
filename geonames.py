import httplib
import simplejson
import sys
from urllib import urlencode

from responsehandlers.element_tree import ElementTreeResponseHandler

# Default GeoNames server to connect to.
DEFAULT_GEONAMES_SERVER = 'ws.geonames.org'
DEFAULT_RESPONSE_HANDLER = ElementTreeResponseHandler


class GeoNames():
    """
    Accessor class for the online GeoNames geographical database. 
    """
    def __init__(self, server=DEFAULT_GEONAMES_SERVER, default_handler=DEFAULT_RESPONSE_HANDLER):
        """
        Create a GeoNames object.
        """
        self.server = server
        self.response_handler = default_handler()
    
    def _api_call(self, method, resource, **kwargs):
        """
        Makes a generic API call to geonames webservice.
        """
        uri = "/%s?%s" %(resource, urlencode(kwargs))
        c = self.get_connection()
        c.request(method, uri)
        response = c.getresponse()
        if not 200 == response.status:
            raise GeoNameException("Expected a 200 reponse but got %s." %(response.status))
        return self.response_handler.get_processed_data(response.read())
                
    def get_connection(self):
        """
        Return a connection object to the webservice.
        """
        c = httplib.HTTPConnection(self.server)
        return c
        
    def search(self, name, country):
        """
        Perform a search for a country's information.
        """
        # we only want exact matches, and we only want one possible match.
        return self._api_call('GET', 'search', name_equals=name, country=country, maxRows=1)
                        
                
class GeoNameException(Exception):
    """
    Error initializing GeoNames accessor.
    """
    pass