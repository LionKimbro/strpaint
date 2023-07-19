
import unittest

import strscan


demo_expectation = [(2, 37, 1, 6, 'foo', '.'),
                    (39, 76, 3, 6, 'bar', '.'),
                    (2, 17, 7, 8, 'baz', '_'),
                    (2, 17, 8, 9, 'boz', '_')]


test1 = "  ..foo..  "
expect1 = [(2,9, 0,1, "foo", ".")]
expect1_line = [(".", 2, 9, "foo")]

test2 = " [..foo..] "
expect2 = [(2,9, 0,1, "foo", ".")]
expect2_line = [(".", 2, 9, "foo")]



# a real life example
test_real = """
    title: ..TITLE.................................................

  working: [.WORKING........](.W..) ! .CLEARW.  run: .....CMD1.....
                                                     _____CMD2_____
 .1. bay1: [.BAY1...........](.B1.) / .CLEAR1.       .....CMD3.....
 _2_ bay2: [_BAY2___________](_B2_) / _CLEAR2_       _____CMD4_____
 .3. bay3: [.BAY3...........](.B3.) / .CLEAR3.
 _4_ bay4: [_BAY4___________](_B4_) / _CLEAR4_  __TRANSFERNOTE__
 .5. bay5: [.BAY5...........](.B5.) / .CLEAR5.

  <INV> -- repository: INVENTORY
  <COMMIT ...> -- repository: COMMIT (w/ commit msg)   <NOCOMMIT> -- roll copy
  <GET ...> -- repository: CHECKOUT (w/ project name)
  <EXPORT> -- export to independent folder
  <DIFF> -- diff vs. last commit
  <LOG> -- log of working directory's project
"""

expect_real = [(11, 67, 1, 2, 'TITLE', '.'),
               (12, 28, 3, 4, 'WORKING', '.'),
               (30, 34, 3, 4, 'W', '.'),
               (38, 46, 3, 4, 'CLEARW', '.'),
               (53, 67, 3, 4, 'CMD1', '.'),
               (53, 67, 4, 5, 'CMD2', '_'),
               (1, 4, 5, 6, '1', '.'),
               (12, 28, 5, 6, 'BAY1', '.'),
               (30, 34, 5, 6, 'B1', '.'),
               (38, 46, 5, 6, 'CLEAR1', '.'),
               (53, 67, 5, 6, 'CMD3', '.'),
               (1, 4, 6, 7, '2', '_'),
               (12, 28, 6, 7, 'BAY2', '_'),
               (30, 34, 6, 7, 'B2', '_'),
               (38, 46, 6, 7, 'CLEAR2', '_'),
               (53, 67, 6, 7, 'CMD4', '_'),
               (1, 4, 7, 8, '3', '.'),
               (12, 28, 7, 8, 'BAY3', '.'),
               (30, 34, 7, 8, 'B3', '.'),
               (38, 46, 7, 8, 'CLEAR3', '.'),
               (1, 4, 8, 9, '4', '_'),
               (12, 28, 8, 9, 'BAY4', '_'),
               (30, 34, 8, 9, 'B4', '_'),
               (38, 46, 8, 9, 'CLEAR4', '_'),
               (48, 64, 8, 9, 'TRANSFERNOTE', '_'),
               (1, 4, 9, 10, '5', '.'),
               (12, 28, 9, 10, 'BAY5', '.'),
               (30, 34, 9, 10, 'B5', '.'),
               (38, 46, 9, 10, 'CLEAR5', '.'),
               (10, 13, 12, 13, None, '.'),
               (7, 10, 13, 14, None, '.'),
               (19, 20, 15, 16, None, '.')]


class TestStrScan(unittest.TestCase):
    
    def setUp(self):
        # Perform any setup actions before each test method
        pass

    def tearDown(self):
        # Perform any cleanup actions after each test method
        pass
    
    def test_demo(self):
        self.assertEqual(strscan.scan(strscan.test),
                         demo_expectation)

    def test_real(self):
        self.assertEqual(strscan.scan(test_real),
                         expect_real)

    def test_1(self):
        self.assertEqual(strscan.scan(test1), expect1)
    
    def test_2(self):
        self.assertEqual(strscan.scan(test2), expect2)
    
    def test_scanline_1(self):
        self.assertEqual(strscan.scanline(test1),
                         expect1_line)
    
    def test_scanline_2(self):
        self.assertEqual(strscan.scanline(test2),
                         expect2_line)


if __name__ == '__main__':
    unittest.main()

