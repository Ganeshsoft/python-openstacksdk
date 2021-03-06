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

import mock
import six

from openstack.object_store.v1 import _proxy
from openstack.object_store.v1 import container
from openstack.object_store.v1 import obj
from openstack import session
from openstack.tests.unit import base
from openstack.tests.unit import fakes
from openstack.tests.unit import test_proxy_base
from openstack import transport


class TestObjectStoreProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestObjectStoreProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_account_metadata_get(self):
        self.verify_head(container.Container, self.proxy.get_account_metadata)

    def test_container_metadata_get(self):
        self.verify_head(container.Container,
                         self.proxy.get_container_metadata, value="container")

    def test_container_delete(self):
        self.verify_delete(self.proxy.delete_container,
                           container.Container, False)

    def test_container_delete_ignore(self):
        self.verify_delete(self.proxy.delete_container,
                           container.Container, True)

    def test_container_create_attrs(self):
        self.verify_create(self.proxy.create_container, container.Container)

    def test_object_metadata_get(self):
        self.verify_head(obj.Object, self.proxy.get_object_metadata,
                         value="object", container="container")

    def _test_object_delete(self, ignore):
        expected_kwargs = {"path_args": {"container": "name"}}
        expected_kwargs["ignore_missing"] = ignore

        self._verify2("openstack.proxy.BaseProxy._delete",
                      self.proxy.delete_object,
                      method_args=["resource"],
                      method_kwargs={"container": "name",
                                     "ignore_missing": ignore},
                      expected_args=[obj.Object, "resource"],
                      expected_kwargs=expected_kwargs)

    def test_object_delete(self):
        self._test_object_delete(False)

    def test_object_delete_ignore(self):
        self._test_object_delete(True)

    def test_object_create_attrs(self):
        self.verify_create(self.proxy.create_object, obj.Object)

    def test_object_get(self):
        self.verify_get(self.proxy.get_object, obj.Object,
                        value=["object"], container="container")


class Test_containers(TestObjectStoreProxy, base.TestTransportBase):

    TEST_URL = fakes.FakeAuthenticator.ENDPOINT

    def setUp(self):
        super(Test_containers, self).setUp()
        self.transport = transport.Transport(accept=transport.JSON)
        self.auth = fakes.FakeAuthenticator()
        self.session = session.Session(self.transport, self.auth)

        self.proxy = _proxy.Proxy(self.session)

        self.containers_body = []
        for i in range(3):
            self.containers_body.append({six.text_type("name"):
                                         six.text_type("container%d" % i)})

#    @httpretty.activate
#    def test_all_containers(self):
#        self.stub_url(httpretty.GET,
#                      path=[container.Container.base_path],
#                      responses=[httpretty.Response(
#                             body=json.dumps(self.containers_body),
#                             status=200, content_type="application/json"),
#                             httpretty.Response(body=json.dumps([]),
#                             status=200, content_type="application/json")])
#
#        count = 0
#        for actual, expected in zip(self.proxy.containers(),
#                                    self.containers_body):
#            self.assertEqual(expected, actual)
#            count += 1
#        self.assertEqual(len(self.containers_body), count)

#    @httpretty.activate
#    def test_containers_limited(self):
#        limit = len(self.containers_body) + 1
#        limit_param = "?limit=%d" % limit
#
#        self.stub_url(httpretty.GET,
#                      path=[container.Container.base_path + limit_param],
#                      json=self.containers_body)
#
#        count = 0
#        for actual, expected in zip(self.proxy.containers(limit=limit),
#                                    self.containers_body):
#            self.assertEqual(actual, expected)
#            count += 1
#
#        self.assertEqual(len(self.containers_body), count)
#        # Since we've chosen a limit larger than the body, only one request
#        # should be made, so it should be the last one.
#        self.assertIn(limit_param, httpretty.last_request().path)

#    @httpretty.activate
#    def test_containers_with_marker(self):
#        marker = six.text_type("container2")
#        marker_param = "marker=%s" % marker
#
#        self.stub_url(httpretty.GET,
#                      path=[container.Container.base_path + "?" +
#                            marker_param],
#                      json=self.containers_body)
#
#        count = 0
#        for actual, expected in zip(self.proxy.containers(marker=marker),
#                                    self.containers_body):
#            # Make sure the marker made it into the actual request.
#            self.assertIn(marker_param, httpretty.last_request().path)
#            self.assertEqual(expected, actual)
#            count += 1
#
#        self.assertEqual(len(self.containers_body), count)
#
#        # Since we have to make one request beyond the end, because no
#        # limit was provided, make sure the last container appears as
#        # the marker in this last request.
#        self.assertIn(self.containers_body[-1]["name"],
#                      httpretty.last_request().path)


class Test_objects(TestObjectStoreProxy, base.TestTransportBase):

    TEST_URL = fakes.FakeAuthenticator.ENDPOINT

    def setUp(self):
        super(Test_objects, self).setUp()
        self.transport = transport.Transport(accept=transport.JSON)
        self.auth = fakes.FakeAuthenticator()
        self.session = session.Session(self.transport, self.auth)

        self.proxy = _proxy.Proxy(self.session)

        self.container_name = six.text_type("my_container")

        self.objects_body = []
        for i in range(3):
            self.objects_body.append({six.text_type("name"):
                                      six.text_type("object%d" % i)})

        # Returned object bodies have their container inserted.
        self.returned_objects = []
        for ob in self.objects_body:
            ob[six.text_type("container")] = self.container_name
            self.returned_objects.append(ob)
        self.assertEqual(len(self.objects_body), len(self.returned_objects))

#    @httpretty.activate
#    def test_all_objects(self):
#        self.stub_url(httpretty.GET,
#                      path=[obj.Object.base_path %
#                            {"container": self.container_name}],
#                      responses=[httpretty.Response(
#                             body=json.dumps(self.objects_body),
#                             status=200, content_type="application/json"),
#                             httpretty.Response(body=json.dumps([]),
#                             status=200, content_type="application/json")])
#
#        count = 0
#        for actual, expected in zip(self.proxy.objects(self.container_name),
#                                    self.returned_objects):
#            self.assertEqual(expected, actual)
#            count += 1
#        self.assertEqual(len(self.returned_objects), count)

#    @httpretty.activate
#    def test_objects_limited(self):
#        limit = len(self.objects_body) + 1
#        limit_param = "?limit=%d" % limit
#
#        self.stub_url(httpretty.GET,
#                      path=[obj.Object.base_path %
#                            {"container": self.container_name} + limit_param],
#                      json=self.objects_body)
#
#        count = 0
#        for actual, expected in zip(self.proxy.objects(self.container_name,
#                                                       limit=limit),
#                                    self.returned_objects):
#            self.assertEqual(expected, actual)
#            count += 1
#
#        self.assertEqual(len(self.returned_objects), count)
#        # Since we've chosen a limit larger than the body, only one request
#        # should be made, so it should be the last one.
#        self.assertIn(limit_param, httpretty.last_request().path)

#    @httpretty.activate
#    def test_objects_with_marker(self):
#        marker = six.text_type("object2")
#       # marker_param = "marker=%s" % marker
#
#        self.stub_url(httpretty.GET,
#                      path=[obj.Object.base_path %
#                            {"container": self.container_name} + "?" +
#                            marker_param],
#                      json=self.objects_body)
#
#        count = 0
#        for actual, expected in zip(self.proxy.objects(self.container_name,
#                                                       marker=marker),
#                                    self.returned_objects):
#            # Make sure the marker made it into the actual request.
#            self.assertIn(marker_param, httpretty.last_request().path)
#            self.assertEqual(expected, actual)
#            count += 1
#
#        self.assertEqual(len(self.returned_objects), count)
#
#        # Since we have to make one request beyond the end, because no
#        # limit was provided, make sure the last container appears as
#        # the marker in this last request.
#        self.assertIn(self.returned_objects[-1]["name"],
#                      httpretty.last_request().path)


class Test_save_object(TestObjectStoreProxy):

    @mock.patch("openstack.object_store.v1._proxy.Proxy.get_object")
    def test_save(self, mock_get):
        the_data = "here's some data"
        mock_get.return_value = the_data
        ob = mock.MagicMock()

        fake_open = mock.mock_open()
        file_path = "blarga/somefile"
        with mock.patch("openstack.object_store.v1._proxy.open",
                        fake_open, create=True):
            self.proxy.save_object(ob, file_path)

        fake_open.assert_called_once_with(file_path, "w")
        fake_handle = fake_open()
        fake_handle.write.assert_called_once_with(the_data)


class Test_copy_object(TestObjectStoreProxy):

    def test_copy_object(self):
        self.assertRaises(NotImplementedError, self.proxy.copy_object)
