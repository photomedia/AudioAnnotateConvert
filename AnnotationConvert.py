#! /usr/bin/env python
import sys
import string
import getopt
import re

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(' -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    with open(inputfile) as f1:
        with open(outputfile, 'w') as f2:
            #f2.write("<Item xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamepaceSchemaLocation=\"avalon_structure.xsd\">\n")   
            #f2.write("<Item>\n")
            lines = f1.readlines()
            line = lines[0]
            next_line = lines[1]
            if line != "\n" and next_line == "\n":
                title=line.rstrip('\n')
            else: #no title found
                title="Untitled"
            f2.write("<Item label=\""+title+"\">\n")
            for i, line in enumerate(lines):
                pattern = '^(\d+:):{0,2}\d+(\.\d+)?'
                test_string = line
                result = re.match(pattern, test_string)
                if result:
                    timecode=line.rstrip('\n')
                    speaker=previous_line.rstrip('\n')
                    label=lines[i+1].rstrip('\n')
                    label=label.replace('"', '&quot;')
                    lookahead = i+4
                    if len(lines) > lookahead :
                        endtimecode = lines[i+4].rstrip('\n')
                    else:
                        endtimecode = ""
                    f2.write("  <Span label=\""+speaker+" "+label+"\" begin=\""+timecode+"\" end=\""+endtimecode+"\" />\n")
                else:
                    previous_line=line
            f2.write("</Item>")

if __name__ == "__main__":
    main(sys.argv[1:])