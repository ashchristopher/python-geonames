import httplib
import simplejson
import sys

from urllib import urlencode
from xml.etree import ElementTree

# Default GeoNames server to connect to.
DEFAULT_GEONAMES_SERVER = 'ws.geonames.org'


class GeoNames():
    API_CALLS = {
        'geoname' : ['search'],
    }
    
    """
    Accessor class for the online GeoNames geographical database. 
    """
    def __init__(self, server=DEFAULT_GEONAMES_SERVER):
        """
        Create a GeoNames object.
        
            server - address of the server which provides REST webservice interface.
        """
        self.server = server
    
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
        return response.read()
                
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
        api_call = 'search'
        # we only want exact matches, and we only want one possible match.
        xml = self._api_call('GET', api_call, name_equals=name, country=country, maxRows=1)
        root_element = ElementTree.XML(xml)
        is_results = root_element.find('totalResultsCount').text
        if not is_results:
            raise GeoNameResultException("No results returned for query.")
        return self._build_results(root_element.findall(self._get_root_element(api_call)))
        
    def _build_results(self, elements):
        results = []
        if not len(elements):
            return results
        for element in elements:
            result = GeoNameResult()
            for fields in element.getchildren():
                result.__setattr__(fields.tag, fields.text)
            results.append(result)
        return results
    
    def _get_root_element(self, api_call):
        """
        Figure out the root element for a particular api call.
        """
        for root, apis in self.API_CALLS.items():
            if api_call in apis:
                return root
        return None
            
    
class GeoNameResult(object):
    """
    Simple object used to hold results from the api call.
    """
    pass
                
                
class GeoNameException(Exception):
    """
    Error initializing GeoNames accessor.
    """
    pass
        
class GeoNameResultException(GeoNameException):
    """
    Error getting results from GeoName webservice.
    """
    pass
