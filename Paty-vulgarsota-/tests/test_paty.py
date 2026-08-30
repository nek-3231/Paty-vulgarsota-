import unittest
from paty.errors import PatyError
from paty.db import init_db

class TestPaty(unittest.TestCase):
    def test_db_init(self):
        try:
            init_db()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"DB init failed: {e}")

if __name__ == '__main__':
    unittest.main()
