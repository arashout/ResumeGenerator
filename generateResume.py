import os
from jinja2 import Environment, FileSystemLoader
import json
import pdfkit
from datetime import datetime
import argparse

# Resume + Template Constants
FIELD_START_DATE = 'startDate'
FIELD_END_DATE = 'endDate'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
CUSTOM_DATE_FORMAT = '%b %Y'
FIELD_POSTFIX = 'Custom'
PATH_CAREER_CUP_DIRECTORY = 'CareerCup'
PATH_CAREER_CUP_TEMPLATE = r'CareerCup/careerCupTemplate.html'


def is_date_field(field: str) -> bool:
    date_fields = [FIELD_START_DATE, FIELD_END_DATE]
    if field in date_fields:
        return True
    else:
        return False


def generate_custom_date_field(field_name: str, date_string: str) -> tuple:
    datetime_obj = datetime.strptime(date_string, DEFAULT_DATE_FORMAT)

    custom_datetime_string = datetime.strftime(datetime_obj, CUSTOM_DATE_FORMAT)
    custom_key = field_name + FIELD_POSTFIX
    return custom_key, custom_datetime_string


def insert_key_value_wrapper(the_obj, func_key_condtion, func_new_key_value):
    """
    This function inserts new key value pairs using 'func_new_key_value' where
    'func_key_condtion' is true

    :param the_obj:
    :param func_key_condtion:
    :param func_new_key_value:
    :return:
    """
    def recursive_explorer(obj):
        if isinstance(obj, list):
            for value in obj:
                recursive_explorer(value)
        elif isinstance(obj, dict):
            copy_keys = []  # Need to copy since we can't insert during iteration
            for key, value in obj.items():
                recursive_explorer(value)
                copy_keys.append(key)

            # Insert new keys if condition met
            for key in copy_keys:
                if func_key_condtion(key):
                    new_key, new_value = func_new_key_value(key, obj[key])
                    obj[new_key] = new_value

    recursive_explorer(the_obj)
    return the_obj


class GenerateResume(object):
    def __init__(self, working_directory: str, path_json_resume: str, path_html_template: str,):
        self.TEMPLATE_ENVIRONMENT = Environment(
            autoescape=False,
            loader=FileSystemLoader(working_directory),
            trim_blocks=False
        )
        self.path_html_template = path_html_template
        self.dict_anon = None
        with open(path_json_resume, 'r') as f:
            self.dict_resume = json.load(f)

    def add_json_anon(self, path):
        with open(path, 'r') as f:
            self.dict_anon = json.load(f)

    def anonymize_resume(self):
        json_resume = json.dumps(self.dict_resume)
        for key, value in self.dict_anon.items():
            json_resume = json_resume.replace(key, value)

        self.dict_resume = json.loads(json_resume)

    def create_html_resume(self, output_html_name: str):
        if self.dict_anon is not None:
            self.anonymize_resume()

        appended_resume = insert_key_value_wrapper(self.dict_resume, is_date_field, generate_custom_date_field)

        with open(output_html_name, 'w') as fp:
            html = self.TEMPLATE_ENVIRONMENT.get_template(self.path_html_template).render(appended_resume)
            fp.write(html)

    def create_pdf_from_html(self, out_pdf_name: str):
        temp_html_path = os.path.join(PATH_CAREER_CUP_DIRECTORY, 'temp.html')
        self.create_html_resume(temp_html_path)
        pdfkit.from_file(temp_html_path, out_pdf_name, options={'page-size': 'Letter'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_json_resume', help='Path to json resume, containing input data for html and pdf resumes')
    parser.add_argument("-a","--path_json_anon", help="Path to json anon dictionary, where:\n"
                        "keys = sensitive information to replace\n"
                        "values = generic text to replace sensitive text"
                        )
    current_directory = os.path.dirname(os.path.abspath(__file__))

    args = parser.parse_args()

    gr = GenerateResume(
        working_directory=current_directory,
        path_json_resume=args.path_json_resume,
        path_html_template=r'CareerCup/careerCupTemplate.html'
    )
    if args.path_json_anon:
        gr.add_json_anon(args.path_json_anon)

    gr.create_pdf_from_html('resume.pdf')
