import unittest
import read
from binascii import unhexlify


class TestReadMethods(unittest.TestCase):

    def test_sync_safe_reader(self):
        self.assertEqual(read.sync_safe_reader(self.to_bytes(120)), 120)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(152)), 24)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(1080)), 568)
        self.assertEqual(read.sync_safe_reader(self.to_bytes(105000)), 19752)
        self.assertEquals(read.sync_safe_reader(self.to_bytes(932938)), 237130)

    def test_seek_string(self):
        self.assertEqual(read.seek_string(b'Walter s\x00'), 'Walter s')
        self.assertEqual(read.seek_string(b'Walter s\x00lew'), 'Walter s')
        self.assertEqual(read.seek_string(b'Walter s'), 0)

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
    def to_bytes (self, val):
        width = val.bit_length()
        width += 8 - ((width % 8) or 8)
        fmt = '%%0%dx' % (width // 4)
        s = unhexlify(fmt % val)
        return s


if __name__ == '__main__':
    unittest.main()
