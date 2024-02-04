#!/usr/bin/python3

# -----------------------
# Author: Farbod Mahdian
# Date: Feb 03 2024
#
# Description:
# This tool helps you to keep track of the jobs that you have applied
# by storing the job description webpage as an HTML file as well as copying your
# template files such as your resume and your cover letter to the same place.
#
# I hope it helps you to find what you deserve :)
#
# Instruction:
# Please update the CONFIG section with the correct paths.
# -----------------------


from datetime import datetime
from os import makedirs, path
from re import compile
from shutil import copy

from requests import get, Response

# --- CONFIG ---

# the full path (absolute path) to the folder/directory that you want to save these data.
# *please create a directory for this purpose first before running the script*
#
# Samples:
# Windows (use \\ instead of \): "C:\\folder1\\foder2\\...\\your_desired_folder_name_to_save_everything_there"
# Linux/Mac: "directory1/directory2/.../your_desired_directory_name_to_save_everything_there"
root_dir_abs_path = 'your_desired_folder_name_to_save_everything_there'

# the list of your template files such as resume and cover letter
#
# Sample:
# required_files = [
#     'the_path_to_your_resume',
#     'the_path_to_your_cover_letter'
# ]
required_files = []

# --------------


def main():
    job_posting_url = input('Please paste the job posting link here: ')
    validate_path(root_dir_abs_path, exit_on_failure=True)

    job_posting_webpage = fetch_webpage(job_posting_url)

    title = extract_title(job_posting_webpage.text)

    curr_date = datetime.now()
    curr_date_formatted = curr_date.strftime("%Y-%b-%d")
    timestamp = str(curr_date.timestamp()).replace('.', '')

    print_log('Creating a directory for the applied job...')
    applied_job_dir = path.join(
        root_dir_abs_path, curr_date_formatted, f'{title}_{timestamp}')
    makedirs(applied_job_dir)

    print_log('Saving the job posting\'s webpage...')
    html_file_path = path.join(applied_job_dir, f'{title}.html')
    with open(html_file_path, 'wb') as html_page:
        html_page.write(job_posting_webpage.content)

    print_log('Copying the required template files...')
    for file_ in required_files:
        if validate_path(file_):
            copy(file_, applied_job_dir)

    print_log('Done!')


def fetch_webpage(url: str) -> Response:
    try:
        print_log('Fetching the job posting\'s webpage...')
        res = get(url)
    except Exception as err:
        print_log(
            f'ERROR: Something went wrong. Please make sure "{url}" is a valid link.\n'
            f'The error: {err}'
        )
        exit(1)

    return res


def validate_path(path_: str, exit_on_failure: bool = False) -> bool:
    if not path.exists(path_):
        log_type = 'ERROR' if exit_on_failure else 'WARNING'
        print_log(f'{log_type}: Please make sure "{path_}" path exists.')

        if exit_on_failure:
            exit(1)
        return False
    return True


def extract_title(context: str) -> str:
    title = "Job_info"

    title_pat = compile(r'<title>(.+)<\/title>')
    is_title = title_pat.findall(context)

    if is_title:
        title = is_title[0]
        title = list(
            map(lambda char_: char_ if str.isalnum(char_) else '_', title))

        title = ''.join(title)
    return title


def print_log(log_: str) -> None:
    print(f'[log] - {log_}')


if __name__ == '__main__':
    main()
