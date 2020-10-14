#! /usr/bin/env python
import sys
import string
import getopt
import re
import xml.etree.ElementTree as ET

def processOneItemXML(Item, f2):
    ItemLabel = Item.get('label')
    line_to_write = ItemLabel+'\n\n'
    f2.write(line_to_write)
    for Span in Item.findall('Span'):
        label = Span.get('label')
        speaker = label.split('.', 1)[0]
        annotation = label.split('.', 1)[1]
        begin = Span.get('begin')
        line_to_write = speaker+'\n'+begin+'\n'+annotation.lstrip()+'\n\n'
        f2.write(line_to_write.encode('utf-8'))

def processOneItem(ItemToProcess, f2):
    #process one Item:
    line = ItemToProcess[0]
    next_line = ItemToProcess[1]
    if line != "\n" and next_line == "\n":
        title=line.rstrip('\n')
    else: #no title found
        title="Untitled"
    f2.write("<Item label=\""+title+"\">\n")
    for i, line in enumerate(ItemToProcess):
        pattern = '^(\d+:):{0,2}\d+(\.\d+)?'
        test_string = line
        result = re.match(pattern, test_string)
        if result:
            timecode=line.rstrip('\n')
            speaker=previous_line.rstrip('\n')
            if (len(ItemToProcess) > (i+1)):
                label=ItemToProcess[i+1].rstrip('\n')
                label=label.replace('"', '&quot;')
            else:
                label="";
            lookahead = i+4
            if len(ItemToProcess) > lookahead :
                endtimecode = ItemToProcess[i+4].rstrip('\n')
            else:
                endtimecode = timecode
            f2.write("  <Span label=\""+speaker+". "+label+"\" begin=\""+timecode+"\" end=\""+endtimecode+"\" />\n")
        else:
            previous_line=line
    f2.write("</Item>")
    #end of process one item


def main(argv):
    inputfile = ''
    outputfile = ''
    reverseConvert = False
    try:
        opts, args = getopt.getopt(argv, "rhi:o:", ["ifile=", "ofile="])
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
        if opt in ("-r"):
            reverseConvert = True
    if (reverseConvert == True):
        #Convert from XML to Text
        with open(inputfile) as f1:
            with open(outputfile, 'w') as f2:
                tree = ET.parse(f1)
                root = tree.getroot()
                if root.tag == "Items":
                    for Item in root.findall('Item'):
                        processOneItemXML(Item, f2)
                else:
                    Item = root
                    processOneItemXML(Item, f2)


    else:
        #Convert from Text to XML
        with open(inputfile) as f1:
            with open(outputfile, 'w') as f2:
                #set the source item
                lines = f1.readlines()
                special_line_indexes = []
                for i, line in enumerate(lines): 
                    if ('END\n' == line):
                        #extract line index for lines that contain END
                        special_line_indexes.append(i + 1)
                length = len(special_line_indexes) 
                #check if multiple files included
                if length>1:
                    startIndex = 0
                    f2.write("<Items>")
                    for i in range(length): 
                        endIndex = special_line_indexes[i]+2
                        #print (str(startIndex)+' '+str(endIndex))
                        ItemToProcess=lines[startIndex:endIndex]
                        processOneItem(ItemToProcess, f2)
                        startIndex=endIndex+1
                    f2.write("</Items>")
                else:
                    processOneItem(lines, f2)
if __name__ == "__main__":
    main(sys.argv[1:])