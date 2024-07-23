from __future__ import annotations

import unittest
from unittest.mock import patch

import requests  # type: ignore
from rea_beta_backend_toolsets.services.proxies.helpers import is_valid
from rea_beta_backend_toolsets.services.proxies.helpers import is_valid_format
from rea_beta_backend_toolsets.services.proxies.helpers import is_valid_request


class TestProxyValidation(unittest.TestCase):

    def test_is_valid_format(self):
        self.assertTrue(is_valid_format('192.168.1.1:8080'))
        self.assertTrue(is_valid_format('255.255.255.255:65535'))
        self.assertFalse(is_valid_format('256.256.256.256:8080'))
        self.assertFalse(is_valid_format('192.168.1.1'))
        self.assertFalse(is_valid_format('192.168.1.1:'))
        self.assertFalse(is_valid_format('192.168.1.1:99999'))
        self.assertFalse(is_valid_format('not_a_proxy'))
        self.assertFalse(is_valid_format(''))
        self.assertFalse(is_valid_format('    '))

    @patch('requests.get')
    def test_is_valid_request(self, mock_get):

        mock_get.return_value.status_code = 200
        self.assertTrue(is_valid_request('http://192.168.1.1:8080'))

        mock_get.return_value.status_code = 500
        self.assertFalse(is_valid_request('http://192.168.1.1:8080'))

        mock_get.side_effect = requests.RequestException
        self.assertFalse(is_valid_request('http://192.168.1.1:8080'))

    @patch('requests.get')
    def test_is_valid(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertTrue(is_valid('192.168.1.1:8080'))

        mock_get.return_value.status_code = 500
        self.assertFalse(is_valid('192.168.1.1:8080'))

        mock_get.side_effect = requests.RequestException
        self.assertFalse(is_valid('192.168.1.1:8080'))

        self.assertFalse(is_valid('256.256.256.256:8080'))
        self.assertFalse(is_valid('192.168.1.1'))


if __name__ == '__main__':
    unittest.main()
