import json
from itertools import accumulate


class FixedWidthSpec:
    """
    Spec class representing a FixedWidthSpec. Accepts a dictionary with the fixed file metadata specification:
    {
       "ColumnNames":"f1, f2, f3, f4, f5, f6, f7, f8, f9, f10",
       "Offsets":"3,12,3,2,13,1,10,13,3,13",
       "InputEncoding":"windows-1252",
       "IncludeHeader":"True",
       "OutputEncoding":"utf-8"
    }
    """
    def __init__(self, config: dict):
        if any([x not in config.keys() for x in
                ("ColumnNames", "Offsets", "InputEncoding", "IncludeHeader", "OutputEncoding")]):
            raise ValueError("Wrong spec provided")

        self.__dict__ = config
        self.Offsets = [0] + [int(x) for x in self.Offsets.split(',')]
        self.ColumnNames = self.ColumnNames.split(',')
        self.ColumnNames = [x.lstrip().rstrip() for x in self.ColumnNames]
        self.IncludeHeader = True if self.IncludeHeader == 'True' else False


class FixedWidthParser:
    """
    FixedWidthParser parses a fixed input file and write it to a delimiter file according to a FixedWidthSpec.
    """
    def __init__(self, spec: FixedWidthSpec, delimiter: str):
        self.spec = spec
        self.delimiter = delimiter

    def _parse_line(self, line, idx) -> str:
        """Parse one fixes input line according to a list of offset tuples"""
        return [line.rstrip()[l:h] for l, h in idx]

    def _parse_file(self, the_input, the_output, idx: list, spec: FixedWidthSpec) -> None:
        """Parses a file line by line and writes the converted delimited file"""
        if spec.IncludeHeader:
            the_output.write(self.delimiter.join(spec.ColumnNames) + "\n")

        for line in the_input:
            parsed_line = self._parse_line(line, idx)
            the_output.write(self.delimiter.join(parsed_line) + "\n")

    def parse(self, input_file, output_file) -> None:
        """Main parse method"""
        acum = list(accumulate(self.spec.Offsets))
        idx = list(zip(acum[:-1], acum[1:]))

        with open(input_file, "r", encoding=self.spec.InputEncoding) as the_input, \
                open(output_file, 'w', encoding=self.spec.OutputEncoding) as the_output:
            self._parse_file(the_input, the_output, idx, self.spec)

