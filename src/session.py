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

    def _format_fields(self, fields: list) -> list[str]:
        """Internal function to format params's methods

        Args:
            fields (list): A list of fields or the list of dicts return by the get_model_fields function

        Returns:
            list[str]: A list of field's value name
        """
        list_fields = []
        if len(fields) == 0 or isinstance(fields[0], str):
            list_fields = fields
        else:
            for field in fields:
                name = field['name']
                list_fields.append(name,)
        return list_fields
    
    def _format_domain(self, modules: list) -> list[tuple]:
        """Internal function to format domain's methods

        Args:
            modules (list): A list of modules name

        Returns:
            list[tuple]: A list of domains withthe OR conditions for each one
        """
        domain = []
        if len(modules) == 0:
            domain = [('model', 'ilike', '')]
        else:
            for i in range(len(modules)-1):
                domain.append('|',)
            for module in modules:
                domain.append(('model', 'ilike', module),)
        return domain
 
    def authenticate(self) -> int:
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

    def get_db_models(self, modules: list=[]) -> list[dict]:
        """A function that returns all the models of a database and his human-readable string

        Args:
            module (list, optional): module name value. Defaults to ''.

        Returns:
            list: a list of dictionaries {'name': name_value, 'model': model_value}
        """
        model = 'ir.model'
        method = 'search_read'
        domain = self._format_domain(modules)       
        params = {'fields' : ['name', 
                              'model',]}
        result = []
        
        for model in self.execute_method(model, method, domain, params):
            result.append({'name': model['name'], 
                           'model': model['model']},)
        return result

    def get_model_fields(self, model: str) -> list[dict]:
        """A function that returns all the fields of a model

        Args:
            model (str): model name in the form module_name.model_name

        Returns:
            list: a list of dictionaries {'name': name_value, 'label': label_value}
        """
        models = 'ir.model.fields'
        method = 'search_read'
        domain = [('model', '=', model)]
        result = []

        for field in self.execute_method(models, method, domain):
            description = 'Empty String'
            if field['field_description']:
                description = field['field_description']
            
            result.append({'label': description,
                           'name': field['name'],},)
        return result

    def retrive_records(self, model: str, fields: list=[]) -> list[dict]:
        """A function that return all the records of a model

        Args:
            model (str): model name in the form module_name.model_name
            fields (list, optional): list of fields for retrive records. Accept the output of get_model_fields function . Defaults to [] for all fields.

        Returns:
            list: a list of dictionaries {'name': name_value, 'label': label_value}
        """
        list_fields = self._format_fields(fields)
        params = {'fields': list_fields}
        result = []

        ids_record = self.execute_method(model, 'search', [])
        for id in ids_record:
            record = self.execute_method(model, 'read', [id], params)
            result.append(record[0])
        return result