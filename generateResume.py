import os
from jinja2 import Environment, FileSystemLoader
import json
import pdfkit

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
    pdfkit.from_file(html_name, pdf_name)

if __name__ == '__main__':
    with open('resume.json', 'r') as f:
        json_resume = json.load(f)

    template_html = 'table_resume.html'
    output_html = 'out.html'
    output_pdf = 'resume.pdf'
    create_index_html(template_html, output_html, json_resume)
    create_pdf_from_html(output_html, output_pdf)
