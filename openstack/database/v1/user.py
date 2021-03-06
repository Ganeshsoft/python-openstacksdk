# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack.database import database_service
from openstack import resource


class User(resource.Resource):
    id_attribute = 'name'
    resource_key = 'user'
    resources_key = 'users'
    base_path = '/instances/%(instance_id)s/users'
    service = database_service.DatabaseService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True

    # path args
    instance_id = resource.prop('instance_id')

    # Properties
    databases = resource.prop('databases')
    name = resource.prop('name')
    _password = resource.prop('password')

    @property
    def password(self):
        try:
            val = self._password
        except AttributeError:
            val = None
        return val

    @password.setter
    def password(self, val):
        self._password = val

    @classmethod
    def create_by_id(cls, session, attrs, r_id=None, path_args=None):
        url = cls._get_url(path_args)
        # Create expects an array of users
        body = {'users': [attrs]}
        resp = session.post(url, service=cls.service, json=body).body
        return resp
