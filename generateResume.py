import os
from jinja2 import Environment, FileSystemLoader
import json
import pdfkit
from xhtml2pdf import pisa   

current_directory = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(current_directory),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(template, file_name, context):
    with open(file_name, 'w') as f:
        html = render_template(template, context)
        f.write(html)


def create_pdf_from_html(html_name, pdf_name):
    pdfkit.from_file(html_name, pdf_name, options={'page-size': 'Letter'})

# Utility function
def convertHtmlToPdf(sourceFilename, outputFilename):
    sourceFile = open(sourceFilename, 'r')
    sourceHtml = sourceFile.read()
    sourceFile.close()
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")
    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

if __name__ == '__main__':
    with open('resume.json', 'r') as f:
        json_resume = json.load(f)

    template_html = 'resume.html'
    output_html = 'out.html'
    output_pdf = 'resume.pdf'
    create_index_html(template_html, output_html, json_resume)
    pisa.showLogging()
    convertHtmlToPdf(output_html, output_pdf)
