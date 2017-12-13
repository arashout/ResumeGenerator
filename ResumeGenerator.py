import os
from jinja2 import Environment, FileSystemLoader
import json
import yaml
import pdfkit
from datetime import datetime
import argparse

# Resume + Template Constants
CUSTOM_DATE_FORMAT = '%b %Y'
PATH_CAREER_CUP_DIRECTORY = 'CareerCup'
PATH_CAREER_CUP_TEMPLATE = r'CareerCup/careerCupTemplate.html'

def dateformat(value: datetime, format=CUSTOM_DATE_FORMAT):
    return value.strftime(format)

class ResumeGenerator(object):
    def __init__(
            self,
            working_directory: str,
            dict_resume: str,
            path_html_template: str,
            dict_anon=None
    ):
        self.TEMPLATE_ENVIRONMENT = Environment(
            autoescape=False,
            loader=FileSystemLoader(working_directory),
            trim_blocks=False
        )
        self.TEMPLATE_ENVIRONMENT.filters['dateformat'] = dateformat
        self.path_html_template = path_html_template
        self.dict_anon = dict_anon
        self.dict_resume = dict_resume

    def create_html_resume(self, output_html_name: str):
        if self.dict_anon is not None:
            raise NotImplementedError

        with open(output_html_name, 'w') as fp:
            html = self.TEMPLATE_ENVIRONMENT.get_template(
                self.path_html_template).render(self.dict_resume)
            fp.write(html)

    def create_pdf_from_html(self, out_pdf_name: str):
        temp_html_path = os.path.join(PATH_CAREER_CUP_DIRECTORY, 'temp.html')
        self.create_html_resume(temp_html_path)
        pdfkit.from_file(temp_html_path, out_pdf_name,
                         options={'page-size': 'Letter'})
