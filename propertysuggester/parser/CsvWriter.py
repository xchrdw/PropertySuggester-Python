import sys
import time
import argparse

from propertysuggester.utils.CompressedFileType import CompressedFileType
from propertysuggester.utils.datatypes import Entity
from propertysuggester.parser import XmlReader


def write_csv(entities, output_file, sep=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type sep: str
    """
    s = u"{1}{0}{2}{0}{3}{0}{4}\n"
    for entity in entities:
        for claim in entity.claims:
            line = s.format(sep, entity.title, claim.property_id, claim.datatype, claim.value).encode("utf-8")
            output_file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="this program converts wikidata XML dumps to CSV data.")
    parser.add_argument("input", help="The XML input file (a wikidata dump), gzip is supported",
                        type=CompressedFileType('r'))
    parser.add_argument("output", help="The CSV output file (default=sys.stdout)", default=sys.stdout, nargs='?',
                        type=CompressedFileType('w'))
    parser.add_argument("-p", "--processes", help="Number of processors to use (default 4)", type=int, default=4)
    args = parser.parse_args()

    start = time.time()
    write_csv(XmlReader.read_xml(args.input, args.processes), args.output)
    print "total time: %.2fs" % (time.time() - start)