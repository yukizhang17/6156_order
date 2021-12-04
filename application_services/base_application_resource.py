from abc import ABC, abstractmethod
from database_services.base_rdb_service import BaseDataResource

class BaseApplicationException(Exception):

    def __init__(self):
        pass


class BaseApplicationResource(ABC):

    def __init__(self):
        pass

    def get_links(cls, resource_data):
        for resource in resource_data:
            address_id = resource.get('id')

            links = []
            address_link = {"rel": "self", "href": "/addresses/" + str(address_id)}
            links.append(address_link)

            users_link = {"rel": "users", "href": "/users?address_id=" + str(address_id)}
            links.append(users_link)

            resource['links'] = links
            return resource_data

    @classmethod
    def get_by_template(cls, db_name, table_name, template, limit=None, offset=None):
        resource = BaseDataResource.find_by_template(db_name, table_name, template, limit, offset)
        # result = self.get_links(resource)
        # print(resource)
        return resource



    @classmethod
    def get_by_resource_id(cls, key_values, field_list):
        pass

    @classmethod
    def create(cls, db_name, table_name, create_data):
        res = BaseDataResource.create(db_name, table_name, create_data)

        return res

    @classmethod
    def update(cls, db_name, table_name, update_data, template):
        res = BaseDataResource.update(db_name, table_name, update_data, template)
        return res

    @classmethod
    def delete(cls, db_name, table_name, template):
        res = BaseDataResource.delete(db_name, table_name, template)
        return res
    
    @classmethod
    def find_in_condition(cls, db_name, table_name, select_vars, in_variable, in_values):
        res = BaseDataResource.find_in_condition(db_name, table_name, select_vars, in_variable, in_values)
        return res

    @classmethod
    @abstractmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    @abstractmethod
    def get_data_resource_info(cls):
        pass


