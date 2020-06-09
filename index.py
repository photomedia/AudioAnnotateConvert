from flask import Flask, request
import re
app = Flask(__name__)

@app.route('/')
def api_root():
    output = """<html>
    <title>SpokenWeb: Convert SW Annotation to Avalon XML</title>
    <meta charset=\"utf-8\">
    <meta name=\"viewport" content="width=device-width, initial-scale=1\">
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
</script>

    </head>
    <body>

    <form id =\"myform\">
    <div class=\"form-group\">
    <label for=\"annotation\">Paste SW Format Annotation:</label>
    <textarea class=\"form-control\" id=\"annotation\" name=\"annotation\" rows=\"20\"></textarea>
    <button id=\"btnSubmit\" type=\"submit\" class=\"btn btn-primary\"> <i class='far fa-arrow-alt-circle-down'></i> Convert to Avalon XML <i class='far fa-arrow-alt-circle-down'></i></button>
     </div>
     </form>

     <textarea id=\"ConvertedAvalonXML\" class=\"form-control\" rows=\"20\">
    """;
    output=output +"""
    </textarea>
    <script>
    $( \"#btnSubmit\" ).click(function( event ) {
        event.preventDefault();
        fetchConversion();
    });
    </script>
    </body></html>""";
    return output


@app.route('/convert', methods = ['POST'])
def api_convert():
    if request.method == 'POST':
        #return ("Received: " + request.headers['Content-Type'] + request.get_data(True, True, False) )
        annotationText = request.get_data(True, True, False);
        convertedAnnotationText = "Conversion Failed";

        lines = annotationText.splitlines();
        line = lines[0]
        next_line = lines[1]
        if line != "\n" and next_line == "":
            title=line.rstrip('\n')
        else: #no title found
            title="Untitled"
        convertedAnnotationText="<Item label=\""+title+"\">\n";
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
                convertedAnnotationText=convertedAnnotationText+"  <Span label=\""+speaker+" "+label+"\" begin=\""+timecode+"\" end=\""+endtimecode+"\" />\n";
            else:
                previous_line=line
        convertedAnnotationText=convertedAnnotationText+"</Item>";

        return (convertedAnnotationText)

if __name__ == '__main__':
    app.run()