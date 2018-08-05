import os
from jinja2 import Environment, FileSystemLoader
import yaml
import pdfkit
from datetime import datetime
import argparse
from ResumeGenerator import ResumeGenerator

# Resume + Template Constants
FIELD_POSTFIX = 'Custom'
PATH_CAREER_CUP_DIRECTORY = 'CareerCup'
PATH_CAREER_CUP_TEMPLATE = r'CareerCup/careerCupTemplate.html'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_resume', help='Path to resume, containing input data for html and pdf resumes')
    parser.add_argument('-a','--path_anon', help='Path to anon key value pairs, where:\n'
                        'keys = sensitive information to replace\n'
                        'values = generic text to replace sensitive text'
                        )
    parser.add_argument('-o', '--path_output', help='Output path including file name and extension')           
    current_directory = os.path.dirname(os.path.abspath(__file__))

    args = parser.parse_args()

    [base_resume_name, extension] = os.path.splitext(args.path_resume)
    
    with open(args.path_resume, 'r') as f:
        if extension == '.yaml':
            dict_resume = yaml.load(f)
        else:
            print('Resume file format not recognized!')
            exit()
    
    dict_anon = None
    if args.path_anon is not None:
        with open(args.path_anon, 'r') as f: 
            if extension == '.yaml':
                dict_anon = yaml.load(f)
            else:
                print('Resume file format not recognized!, please use YAML')
                exit()

    gr = ResumeGenerator(
        working_directory=current_directory,
        dict_resume=dict_resume,
        path_html_template=r'CareerCup/careerCupTemplate.html',
        dict_anon=dict_anon

    )
    if args.path_output is not None:
        gr.create_pdf_from_html(args.path_output)
