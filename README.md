# AudioAnnotateConvert
Python Script to Convert Audio Annotation Files

Takes the following formats as input:

 * SpokenWeb Text format

Outputs the follwoing format:

 * Avalon XML
 
 The script can also perform the reverse conversion, taking in Avalon XML file and converting to SpokenWeb Text format.
 
 
##  Metadata Conversion

When converting to Avalon XML, the result of conversion is always valid XML.  If source of conversion is one file only, the result is also a fully conforming <Item> as per Avalon XSD.  

###  Multi-file annotations
In case of multi-file source file (annotations that include time stamps from multiple files), the resulting Avalon XSD <i>&lt;Item&gt;</i> tags are placed inside a root <i>&lt;Items&gt;</i> tag, since valid XML requires a single root.  For example:
  
 * Source: https://github.com/photomedia/AudioAnnotateConvert/blob/master/sample4.txt
 * Result: https://github.com/photomedia/AudioAnnotateConvert/blob/master/sample4output.xml
  
It is important to note that multi-file annotation descriptions are not currently supported by Avalon Media System, so this multi-file markup would have to be pre-parsed prior to import into Avalon. 

##  Usage

This script is available as downloadable command line script and/or it can be used online directly without the need for downloading.

### Command Line

Use following command line to run a conversion of SpokenWeb Text formatted "input.txt" file into Avalon XML formatted "test.xml" result:

<code>python AnnotationConvert.py -i input.txt -o test.xml</code>

Use the follwoing command line to run a reverse conversion of Avalon XML formatted "input.xml" file into SpokenWeb Text formatted "output.txt" file.

<code>python AnnotationConvert.py -r -i input.xml -o output.txt</code>

### Online

The script is also available as a Flask web application here: https://photomedia.pythonanywhere.com/
You can just paste in your SpokenWeb Text annotations and have the Avalon XML result from the online form.
You can also paste in Avalon XML and convert it to SpokenWeb Text.

##  Requirements

AnnotationConvert is a Python script that should run using Python 2 or 3.  The development and testing for the Flask app was done on Python 3.5.  

The script is also accessible as an online form, so it can be used with a Web Browser only.
