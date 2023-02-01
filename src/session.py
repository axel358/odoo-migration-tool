from xmlrpc import client

class Session():
    
    def __init__(self, username: str, password: str , url: str, db: str):
        """A class to store session information for use with XMLRPC client

        Args:
            username (str): user of a odoo database
            password (str): login password for user
            url (str): url direction for an odoo service
            db (str): database name
        """
        self.username = username
        self.password = password
        self.url = url
        self.db = db
        self.models_endpoint = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        self.uid = None
 
    def authenticate(self):
        """A function to authenticate the user for get access to execute methods

        Returns:
            int: user id (uid)
        """
        common_endpoint = client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common_endpoint.authenticate(self.db, self.username, self.password, {})
        return self.uid

    def execute_method(self, model: str, method: str, domain: list, params: dict={}):
        """A function to execute methods on the database's models

        Args:
            model (str): the model name
            method (str): the method name
            domain (list): an array/list of parameters passed by position
            params (dict, optional): a mapping/dict of parameters to pass by keyword. Defaults to {}.

        Returns:
            list: depend of the type of method
        """
        if not self.uid:
            return 'Not Authenticated'
        result = self.models_endpoint.execute_kw(self.db, self.uid, self.password, model, method, [domain], params) 
        return result