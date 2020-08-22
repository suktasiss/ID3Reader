import unittest
import read


class TestReadMethods(unittest.TestCase):

    def test_sync_safe_reader(self):
        self.assertEqual(read.sync_safe_reader(self.to_bytes(120)), 120)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(152)), 24)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(1080)), 568)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(105000)), 19752)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    @unittest.skip("reason for skipping")
    def to_bytes(self, number):
        length = len(bytes([number]))
        if length < 4:
            numb_array = [[number]]
            while length < 4:
                numb_array.insert(0, 0)
            number = bytes(numb_array)
        else:
            number = bytes([number])
        return number


if __name__ == '__main__':
    unittest.main()
