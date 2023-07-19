
import unittest

import strpaint


class MyTest(unittest.TestCase):
    def setUp(self):
        # Perform any setup actions before each test method
        strpaint.reset()

    def tearDown(self):
        # Perform any cleanup actions after each test method
        pass

    def test_clip(self):
        strpaint.clip(5,5, 10,8)
        self.assertEqual(strpaint.clip(), (5,5,10,8))

    def test_clipwh(self):
        strpaint.clip(5,5, 10,8)
        self.assertEqual(strpaint.clipwh(), (5,5, 5,3))


if __name__ == '__main__':
    unittest.main()
