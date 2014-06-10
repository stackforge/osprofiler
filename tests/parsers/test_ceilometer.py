# Copyright 2014 Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from osprofiler.parsers import ceilometer

from tests import test


class CeilometerParserTestCase(test.TestCase):

    def test_build_empty_tree(self):
        self.assertEqual(ceilometer._build_tree({}), [])

    def test_build_complex_tree(self):
        test_input = {
            "2": {"parent_id": "0", "trace_id": "2", "info": {"started": 1}},
            "1": {"parent_id": "0", "trace_id": "1", "info": {"started": 0}},
            "21": {"parent_id": "2", "trace_id": "21", "info": {"started": 6}},
            "22": {"parent_id": "2", "trace_id": "22", "info": {"started": 7}},
            "11": {"parent_id": "1", "trace_id": "11", "info": {"started": 1}},
            "113": {"parent_id": "11", "trace_id": "113",
                    "info": {"started": 3}},
            "112": {"parent_id": "11", "trace_id": "112",
                    "info": {"started": 2}},
            "114": {"parent_id": "11", "trace_id": "114",
                    "info": {"started": 5}}
        }

        expected_output = [
            {
                "parent_id": "0",
                "trace_id": "1",
                "info": {"started": 0},
                "children": [
                    {
                        "parent_id": "1",
                        "trace_id": "11",
                        "info": {"started": 1},
                        "children": [
                            {"parent_id": "11", "trace_id": "112",
                             "info": {"started": 2}, "children": []},
                            {"parent_id": "11", "trace_id": "113",
                             "info": {"started": 3}, "children": []},
                            {"parent_id": "11", "trace_id": "114",
                             "info": {"started": 5}, "children": []}
                        ]
                    }
                ]
            },
            {
                "parent_id": "0",
                "trace_id": "2",
                "info": {"started": 1},
                "children": [
                    {"parent_id": "2", "trace_id": "21",
                     "info": {"started": 6}, "children": []},
                    {"parent_id": "2", "trace_id": "22",
                     "info": {"started": 7}, "children": []}
                ]
            }
        ]

        self.assertEqual(ceilometer._build_tree(test_input), expected_output)

    def test_parse_notifications(self):
        samples = [
            {
                "id": "896f5e52-d4c9-11e3-a117-46c0b36ac153",
                "metadata": {
                    "base_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                    "event_type": "profiler.nova",
                    "host": "osapi_compute.0.0.0.0",
                    "name": "WSGI-stop",
                    "parent_id": "82281b35-63aa-45fc-8578-5a32a66370ab",
                    "trace_id": "837eb0bd-323a-4e3f-b223-3be78ad86aab"
                },
                "meter": "WSGI-stop",
                "project_id": None,
                "recorded_at": "2014-05-06T02:53:03.110724",
                "resource_id": "profiler",
                "source": "openstack",
                "timestamp": "2014-05-06T02:52:59.357020",
                "type": "gauge",
                "unit": "sample",
                "user_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                "volume": 1.0
            },
            {
                "id": "895043a0-d4c9-11e3-a117-46c0b36ac153",
                "metadata": {
                    "base_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                    "event_type": "profiler.nova",
                    "host": "osapi_compute.0.0.0.0",
                    "name": "WSGI-start",
                    "parent_id": "82281b35-63aa-45fc-8578-5a32a66370ab",
                    "trace_id": "837eb0bd-323a-4e3f-b223-3be78ad86aab"
                },
                "meter": "WSGI-start",
                "project_id": None,
                "recorded_at": "2014-05-06T02:53:03.020620",
                "resource_id": "profiler",
                "source": "openstack",
                "timestamp": "2014-05-06T02:52:59.225552",
                "type": "gauge",
                "unit": "sample",
                "user_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                "volume": 1.0
            },

            {
                "id": "89558414-d4c9-11e3-a117-46c0b36ac153",
                "metadata": {
                    "base_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                    "event_type": "profiler.nova",
                    "host": "osapi_compute.0.0.0.0",
                    "info.db:multiparams": "(immutabledict({}),)",
                    "info.db:params": "{}",
                    "name": "nova.db-start",
                    "parent_id": "837eb0bd-323a-4e3f-b223-3be78ad86aab",
                    "trace_id": "f8ab042e-1085-4df2-9f3a-cfb6390b8090"
                },
                "meter": "nova.db-start",
                "project_id": None,
                "recorded_at": "2014-05-06T02:53:03.038692",
                "resource_id": "profiler",
                "source": "openstack",
                "timestamp": "2014-05-06T02:52:59.273422",
                "type": "gauge",
                "unit": "sample",
                "user_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                "volume": 1.0
            },
            {
                "id": "892d3018-d4c9-11e3-a117-46c0b36ac153",
                "metadata": {
                    "base_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                    "event_type": "profiler.generic",
                    "host": "nova-conductor.ubuntu",
                    "name": "nova.db-stop",
                    "parent_id": "aad4748f-99d5-45c8-be0a-4025894bb3db",
                    "trace_id": "8afee05d-0ad2-4515-bd03-db0f2d30eed0"
                },
                "meter": "nova.db-stop",
                "project_id": None,
                "recorded_at": "2014-05-06T02:53:02.894015",
                "resource_id": "profiler",
                "source": "openstack",
                "timestamp": "2014-05-06T02:53:00.473201",
                "type": "gauge",
                "unit": "sample",
                "user_id": "f5587500-07d1-41a0-b434-525d3c28ac49",
                "volume": 1.0
            }
        ]

        excepted = {
            "info": {
                "finished": 1247,
                "name": "total",
                "started": 0
            },
            "children": [
                {
                    "info": {
                        "finished": 131,
                        "host": "osapi_compute.0.0.0.0",
                        "name": "WSGI",
                        "service": "nova",
                        "started": 0
                    },
                    "parent_id": "82281b35-63aa-45fc-8578-5a32a66370ab",
                    "trace_id": "837eb0bd-323a-4e3f-b223-3be78ad86aab",
                    "children": [{
                        "children": [],
                        "info": {
                            "finished": 47,
                            "host": "osapi_compute.0.0.0.0",
                            "info.db:multiparams": "(immutabledict({}),)",
                            "info.db:params": "{}",
                            "name": "nova.db",
                            "service": "nova",
                            "started": 47
                        },

                        "parent_id": "837eb0bd-323a-4e3f-b223-3be78ad86aab",
                        "trace_id": "f8ab042e-1085-4df2-9f3a-cfb6390b8090"
                    }]
                },
                {
                    "children": [],
                    "info": {
                        "finished": 1247,
                        "host": "nova-conductor.ubuntu",
                        "name": "nova.db",
                        "service": "generic",
                        "started": 1247
                    },
                    "parent_id": "aad4748f-99d5-45c8-be0a-4025894bb3db",
                    "trace_id": "8afee05d-0ad2-4515-bd03-db0f2d30eed0"
                }
            ]
        }

        self.assertEqual(ceilometer.parse_notifications(samples), excepted)
