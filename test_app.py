import json
import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app import Handler


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Port 0 lets the operating system choose an available port.
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{port}"

        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True,
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health(self):
        with urlopen(f"{self.base_url}/health", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                json.load(response),
                {"status": "healthy"},
            )

    def test_version(self):
        with urlopen(f"{self.base_url}/version", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                json.load(response),
                {"version": "1.0.0"},
            )

    def test_unknown_path(self):
        with self.assertRaises(HTTPError) as context:
            urlopen(f"{self.base_url}/wrong", timeout=5)

        with context.exception as response:
            self.assertEqual(response.code, 404)
            self.assertEqual(
                json.load(response),
                {"error": "Not found"},
            )


if __name__ == "__main__":
    unittest.main()
