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

import uuid

from openstack.network.v2 import network
from openstack.network.v2 import port
from openstack.network.v2 import subnet
from openstack.tests.functional import base


class TestPort(base.BaseFunctionalTest):

    NET_NAME = uuid.uuid4().hex
    SUB_NAME = uuid.uuid4().hex
    PORT_NAME = uuid.uuid4().hex
    UPDATE_NAME = uuid.uuid4().hex
    IPV4 = 4
    CIDR = "10.100.0.0/24"
    NET_ID = None
    SUB_ID = None
    PORT_ID = None

    @classmethod
    def setUpClass(cls):
        super(TestPort, cls).setUpClass()
        net = cls.conn.network.create_network(name=cls.NET_NAME)
        assert isinstance(net, network.Network)
        cls.assertIs(cls.NET_NAME, net.name)
        cls.NET_ID = net.id
        sub = cls.conn.network.create_subnet(name=cls.SUB_NAME,
                                             ip_version=cls.IPV4,
                                             network_id=cls.NET_ID,
                                             cidr=cls.CIDR)
        assert isinstance(sub, subnet.Subnet)
        cls.assertIs(cls.SUB_NAME, sub.name)
        cls.SUB_ID = sub.id
        prt = cls.conn.network.create_port(name=cls.PORT_NAME,
                                           network_id=cls.NET_ID)
        assert isinstance(prt, port.Port)
        cls.assertIs(cls.PORT_NAME, prt.name)
        cls.PORT_ID = prt.id

    @classmethod
    def tearDownClass(cls):
        sot = cls.conn.network.delete_port(cls.PORT_ID, ignore_missing=False)
        cls.assertIs(None, sot)
        sot = cls.conn.network.delete_subnet(cls.SUB_ID, ignore_missing=False)
        cls.assertIs(None, sot)
        sot = cls.conn.network.delete_network(cls.NET_ID, ignore_missing=False)
        cls.assertIs(None, sot)

    def test_find(self):
        sot = self.conn.network.find_port(self.PORT_NAME)
        self.assertEqual(self.PORT_ID, sot.id)

    def test_get(self):
        sot = self.conn.network.get_port(self.PORT_ID)
        self.assertEqual(self.PORT_ID, sot.id)
        self.assertEqual(self.PORT_NAME, sot.name)
        self.assertEqual(self.NET_ID, sot.network_id)

    def test_list(self):
        ids = [o.id for o in self.conn.network.ports()]
        self.assertIn(self.PORT_ID, ids)

    def test_updta(self):
        sot = self.conn.network.update_port(self.PORT_ID,
                                            name=self.UPDATE_NAME)
        self.assertEqual(self.UPDATE_NAME, sot.name)
