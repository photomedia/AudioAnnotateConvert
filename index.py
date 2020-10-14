from flask import Flask, request
from flask_cors import CORS
import xml.etree.ElementTree as ET

import re
app = Flask(__name__)
cors = CORS(app)

def processOneItemXML(Item):
    ItemLabel = Item.get('label')
    line_to_write = ItemLabel+'\n\n'
    convertedAnnotationText=line_to_write
    for Span in Item.findall('Span'):
        label = Span.get('label')
        speaker = label.split('.', 1)[0]
        annotation = label.split('.', 1)[1]
        begin = Span.get('begin')
        line_to_write = speaker+'\n'+begin+'\n'+annotation.lstrip()+'\n\n'
        convertedAnnotationText=convertedAnnotationText+line_to_write
    return(convertedAnnotationText)

def processOneItem(ItemToProcess):
    #process one Item:
    line = ItemToProcess[0]
    next_line = ItemToProcess[1]
    if line != "\n" and next_line == "":
        title=line.rstrip('\n')
    else: #no title found
        title="Untitled"
    convertedAnnotationText="<Item label=\""+title+"\">\n";
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
            convertedAnnotationText=convertedAnnotationText+"  <Span label=\""+speaker+". "+label+"\" begin=\""+timecode+"\" end=\""+endtimecode+"\" />\n";
        else:
            previous_line=line
    convertedAnnotationText=convertedAnnotationText+"</Item>";
    return (convertedAnnotationText)

@app.route('/')
def api_root():
    output = """<html>
    <title>SpokenWeb: Convert SW Annotation to Avalon XML</title>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <head>
    <script src=\"https://kit.fontawesome.com/a076d05399.js\"></script>
    <script src=\"https://code.jquery.com/jquery-3.3.1.min.js\" crossorigin=\"anonymous\"></script>
    <script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js\" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49\" crossorigin=\"anonymous\"></script>

    <link rel=\"stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css\" integrity=\"sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO\" crossorigin=\"anonymous\">
    <script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js\" integrity=\"sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy\" crossorigin=\"anonymous\"></script>

<script>

function fetchConversion() {
    var myform = document.getElementById(\"myform\");
    var fd = new FormData(myform );
    var annotation = document.getElementById(\"annotation\").value;
    $.ajax({
        url: "/convert",
        data: annotation,
        cache: false,
        processData: false,
        contentType: 'text/plain',
        dataType: 'xml',
        type: 'POST',
        success: function (result) {
            $('#ConvertedAvalonXML').val((new XMLSerializer()).serializeToString(result));
        }
    })
}

function fetchConversionToText() {
    var myform = document.getElementById(\"myform\");
    var fd = new FormData(myform );
    var annotation = document.getElementById(\"ConvertedAvalonXML\").value;
    $.ajax({
        url: "/convertToText",
        data: annotation,
        cache: false,
        processData: false,
        contentType: 'xml',
        dataType: 'text',
        type: 'POST',
        success: function (result) {
            $('#annotation').val(result);
        }
    })
}
</script>

    </head>
    <body>

    <form id =\"myform\">
    <div class=\"form-group\">
    <label for=\"annotation\">Paste SW Format Annotation:</label>
    <textarea class=\"form-control\" id=\"annotation\" name=\"annotation\" rows=\"12\"></textarea>
    <button id=\"btnSubmit\" type=\"submit\" class=\"btn btn-primary\"> <i class='far fa-arrow-alt-circle-down'></i> Convert to Avalon XML <i class='far fa-arrow-alt-circle-down'></i></button>
    <button id=\"copyButtonText\" type="button" style="float:right" class=\"btn btn-default\"><i class="fa fa-clone" aria-hidden="true"></i> select & copy Text</button>
     </div>

     <button id=\"copyButton\" type="button" class=\"btn btn-default\"><i class="fa fa-clone" aria-hidden="true"></i> select & copy XML</button>
     <button id=\"btnSubmitToText\" type=\"submit\" class=\"btn btn-primary\" style="float:right"> <i class='far fa-arrow-alt-circle-up'></i> Convert to Text <i class='far fa-arrow-alt-circle-up'></i></button>
     <textarea id=\"ConvertedAvalonXML\" class=\"form-control\" rows=\"10\">
    """;
    output=output +"""
    </textarea>
    </form>
    <br />
    Source Code: <a href=\"https://github.com/photomedia/AudioAnnotateConvert\">https://github.com/photomedia/AudioAnnotateConvert</a>
    <script>
    $( \"#btnSubmit\" ).click(function( event ) {
        event.preventDefault();
        fetchConversion();
    });


    $( \"#btnSubmitToText\" ).click(function( event ) {
        event.preventDefault();
        fetchConversionToText();
    });

   $(\"#copyButton\").click(function(){
    $(\"#ConvertedAvalonXML\").select();
    document.execCommand('copy');
   });

   $(\"#copyButtonText\").click(function(){
    $(\"#annotation\").select();
    document.execCommand('copy');
   });

    </script>
    </body></html>""";
    return output


@app.route('/convert', methods = ['POST'])
def api_convert():
    if request.method == 'POST':
        #return ("Received: " + request.headers['Content-Type'] + request.get_data(True, True, False) )
        annotationText = request.get_data(True, True, False);
        convertedAnnotationText = "";

        lines = annotationText.splitlines();

        special_line_indexes = []
        for i, line in enumerate(lines):
            if ('END' == line):
                #extract line index for lines that contain END
                special_line_indexes.append(i + 1)
        length = len(special_line_indexes)
        #check if multiple files included
        if length>1:
            startIndex = 0
            convertedAnnotationText=convertedAnnotationText+"<Items>"
            for i in range(length):
                endIndex = special_line_indexes[i]+2
                #print (str(startIndex)+' '+str(endIndex))
                ItemToProcess=lines[startIndex:endIndex]
                convertedAnnotationText=convertedAnnotationText+processOneItem(ItemToProcess)
                startIndex=endIndex+1
            convertedAnnotationText=convertedAnnotationText+"</Items>"
        else:
            convertedAnnotationText=processOneItem(lines)

        return (convertedAnnotationText)

@app.route('/convertToText', methods = ['POST'])
def api_convertToText():
    if request.method == 'POST':
        #return ("Received: " + request.headers['Content-Type'] + request.get_data(True, True, False) )
        annotationText = request.get_data(True, True, False);
        convertedAnnotationText = "";

        root = ET.fromstring(annotationText)

        if root.tag == "Items":
            for Item in root.findall('Item'):
                convertedAnnotationText=convertedAnnotationText+processOneItemXML(Item)
        else:
            Item = root
            convertedAnnotationText=processOneItemXML(Item)

        return (convertedAnnotationText)

if __name__ == '__main__':
    app.run()