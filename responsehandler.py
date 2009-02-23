class ResponseHandler(object):
    """
    Abstract(-like) class used to define a response handler 
    object.
    
    A response handler is used to format or interperet api 
    call data for use.
    """
    def get_processed_data(self, input):
        """
        This method should accept an input variable, process 
        as needed, and return the data in an expected format.
        """
        import inspect
        _method = inspect.getouterframes(inspect.currentframe())[0][3]
        raise NotImplementedError(_method + " method must be implemented in subclass.");

class HandlerException(Exception):
    """
    Error getting results from GeoName webservice.
    """
    pass
