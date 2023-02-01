from xmlrpc import client

class Session():
    def __init__(self, username: str, password: str , url: str, db: str):
        self.username = username
        self.password = password
        self.url = url
        self.db = db
        self.common_endpoint = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.models_endpoint = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        self.uid = None
 
    def authenticate(self):
        self.uid = self.common_endpoint.authenticate(self.db, self.username, self.password, {})
        return '%s' % self.uid
    
    def get_db_fields(self):
        if self.uid:
            return self.models_endpoint.execute_kw(self.db, self.uid, self.password, 'ir.model', 'search_read',[[]], {'fields' : ['name', 'model']})
        else: return 'Not Authenticated Yet' 