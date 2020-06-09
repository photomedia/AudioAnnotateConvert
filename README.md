# AudioAnnotateConvert
Python Script to Convert Audio Annotation Files

Takes the following formats as input:

 * Transcriva (transcription software for MAC)

Outputs the follwoing format:

 * Avalon XML

##  Usage

This script is available as downloadable command line script and/or it can be used online directly without the need for downloading.

### Command Line

Use following command line to run a conversion of "input.txt" file into "test.xml" result:

python AnnotationConvert.py -i input.txt -o test.xml

### Online

The script is also available as a Flask web application here: https://photomedia.pythonanywhere.com/
You can just paste in your SW annotations and have the Avalon XML result from the online form.

##  Requirements

AnnotationConvert is a Python script that should run using Python 2 or 3

The script is also accessible as an online form, so it can be used with a Web Browser only.
