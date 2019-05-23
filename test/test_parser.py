import unittest
import sys, os
from io import StringIO
import tempfile

testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from parser import FixedWidthSpec, FixedWidthParser


class FixedWidthSpecTest(unittest.TestCase):

    def test_correct_spec(self):
        spec_dict = {'ColumnNames': 'f1, f2, f3, f4, f5, f6, f7, f8, f9, f10',
                     'Offsets': '3,12,3,2,13,1,10,13,3,13',
                     'InputEncoding': 'windows-1252',
                     'IncludeHeader': 'True',
                     'OutputEncoding': 'utf-8'}
        spec = FixedWidthSpec(spec_dict)

        self.assertEqual(spec.ColumnNames, ["f1","f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10"])
        self.assertEqual(spec.InputEncoding, "windows-1252")
        self.assertEqual(spec.IncludeHeader, True)
        self.assertEqual(spec.OutputEncoding, "utf-8")
        self.assertEqual(spec.Offsets, [0, 3, 12, 3, 2, 13, 1, 10, 13, 3, 13])

    def test_incorrect_spec(self):
        spec_dict = {'ColumnNames': 'f1, f2, f3, f4, f5, f6, f7, f8, f9, f10',
                     'InputEncoding': 'windows-1252',
                     'IncludeHeader': 'True',
                     'OutputEncoding': 'utf-8'}

        with self.assertRaises(ValueError) as context:
            FixedWidthSpec(spec_dict)

        self.assertEqual("Wrong spec provided",str(context.exception))


class FixedWidthParserParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.input_file = tempfile.NamedTemporaryFile("w")
        cls.output_file = tempfile.NamedTemporaryFile("r")
        cls.input_file.write("ABCdefghijklmnoPQR\n")
        cls.input_file.write("STUvwxyzabcdefgHIJ")
        cls.input_file.flush()


    @classmethod
    def tearDownClass(cls) -> None:
        cls.input_file.close()
        cls.output_file.close()


    def setUp(self) -> None:
        spec_dict = {'ColumnNames': 'f1, f2, f3',
                     'Offsets': '3,12,3',
                     'InputEncoding': 'windows-1252',
                     'IncludeHeader': 'False',
                     'OutputEncoding': 'utf-8'}
        self.spec = FixedWidthSpec(spec_dict)
        self.parser = FixedWidthParser(self.spec, ',')

    def test_parse_line(self):
        idx = [ (0, 3), (3, 15), (15, 18) ]
        parsed_str = self.parser._parse_line("ABCdefghijklmnoPQR", idx)
        self.assertEqual(parsed_str,["ABC","defghijklmno","PQR"])


    def test_parse_file(self):
        infile = StringIO()
        outfile = StringIO()
        idx = [(0, 3), (3, 15), (15, 18)]
        infile.write("ABCdefghijklmnoPQR\n")
        infile.write("STUvwxyzabcdefgHIJ")
        infile.flush()
        infile.seek(0)
        self.parser._parse_file(infile, outfile, idx, self.spec)
        content = outfile.getvalue()
        self.assertEqual(content, "ABC,defghijklmno,PQR\nSTU,vwxyzabcdefg,HIJ\n")

    def test_parse_file_with_headers(self):
        infile = StringIO()
        outfile = StringIO()
        idx = [(0, 3), (3, 15), (15, 18)]
        self.spec.IncludeHeader = True
        infile.write("ABCdefghijklmnoPQR\n")
        infile.write("STUvwxyzabcdefgHIJ")
        infile.flush()
        infile.seek(0)
        self.parser._parse_file(infile, outfile, idx, self.spec)
        content = outfile.getvalue()
        self.assertEqual(content, "f1,f2,f3\nABC,defghijklmno,PQR\nSTU,vwxyzabcdefg,HIJ\n")

    def test_parser(self):
        print("test")
        self.parser.parse(FixedWidthParserParserTest.input_file.name, FixedWidthParserParserTest.output_file.name)
        FixedWidthParserParserTest.output_file.flush()
        FixedWidthParserParserTest.output_file.seek(0)
        content = FixedWidthParserParserTest.output_file.read()
        self.assertEqual(content, "ABC,defghijklmno,PQR\nSTU,vwxyzabcdefg,HIJ\n")

if __name__ == '__main__':
    unittest.main()
