import unittest, os, json

class TestCompetitiveSuite(unittest.TestCase):
    def test_metrics_integrity(self):
        self.assertTrue(os.path.exists('METRICS.json'))
        with open('METRICS.json', 'r') as f:
            data = json.load(f)
        self.assertIn('tokens_per_sec', data)

    def test_security_policy_exists(self):
        self.assertTrue(os.path.exists('SECURITY.md'))

if __name__ == '__main__':
    unittest.main()
