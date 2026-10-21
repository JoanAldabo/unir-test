import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


def _get(path):
    url = f"{BASE_URL}{path}"
    try:
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        return response.status, response.read().decode()
    except HTTPError as e:
        return e.code, e.read().decode()


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        status, body = _get("/calc/add/2/2")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "4")

    def test_api_add_invalid_parameter_returns_400(self):
        status, _ = _get("/calc/add/a/2")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_substract(self):
        status, body = _get("/calc/substract/5/3")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "2")

    def test_api_substract_invalid_parameter_returns_400(self):
        status, _ = _get("/calc/substract/a/3")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_multiply(self):
        status, body = _get("/calc/multiply/3/4")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "12")

    def test_api_multiply_invalid_parameter_returns_400(self):
        status, _ = _get("/calc/multiply/a/4")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_divide(self):
        status, body = _get("/calc/divide/6/3")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "2.0")

    def test_api_divide_by_zero_returns_400(self):
        status, _ = _get("/calc/divide/1/0")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_power(self):
        status, body = _get("/calc/power/2/3")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "8.0")

    def test_api_power_invalid_domain_returns_400(self):
        status, _ = _get("/calc/power/-8/0.5")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_sqrt(self):
        status, body = _get("/calc/sqrt/4")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "2.0")

    def test_api_sqrt_negative_returns_400(self):
        status, _ = _get("/calc/sqrt/-4")
        self.assertEqual(status, http.client.BAD_REQUEST)

    def test_api_log10(self):
        status, body = _get("/calc/log10/100")
        self.assertEqual(status, http.client.OK)
        self.assertEqual(body, "2.0")

    def test_api_log10_non_positive_returns_400(self):
        status, _ = _get("/calc/log10/0")
        self.assertEqual(status, http.client.BAD_REQUEST)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
