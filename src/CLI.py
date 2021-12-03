import os.path

from InquirerPy import prompt
from InquirerPy.exceptions import InvalidArgument
from InquirerPy.validator import PathValidator

from src import data_manager


class CLI:
    def __init__(self):
        pass


def get_colour(colour_type):
    colours = {
        'Alert': '#dc3545',
        'Success': '#198754',
        'Warning': '#ffc107'
    }
    return colours[colour_type]


def first_menu():
    var = [
        {
            'message': 'Default file not found! What would you like to do?',
            'type': 'list',
            'when': lambda _: not os.path.exists(data_manager.FileData().filepath),
            'choices': ['Select existing file',
                        'Create new file',
                        'Exit'],
            'name': 'init'
        },
        {
            'message': 'Enter the filepath to upload:',
            'type': 'filepath',
            'when': lambda _: _['init'] == 'Select existing file',
            'validate': PathValidator(),
            'only_files': True,
            'name': 'upload'
        },
        {
            'message': 'Enter the file name, press return to use default:',
            'type': 'input',
            'when': lambda _: _['init'] == 'Create new file',
            'name': 'create'
        }
    ]
    return inquirer(var)


def second_menu():
    var = [
        {
            'message': 'What would you like to do?',
            'type': 'list',
            'choices': [
                'Get login',
                'Add login',
                'Del login',
                'Import data',
                'Export data',
                'Settings',
                'Exit'
            ],
            'name': 'main'
        },
        {
            'message': 'Would you like to save changes?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Exit',
            'choices': [
                'Cancel',
                'No',
                'Yes'
            ],
            'name': 'save'
        },
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Entry name?',
         'name': 'login_name'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login' and _['loginName'] != '', 'message': 'URI?',
         'name': 'login_uri'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login' and _['loginName'] != '',
         'message': 'Username?', 'name': 'login_username'},
        {
            'message': 'Import from?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Import data',
            'name': 'import',
            'choices': [
                'Back',
                'Bitwarden (unencrypted)',
                'PyPass (unencrypted)'
            ]
        },
        {
            'message': 'Export to?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Export data',
            'name': 'export',
            'choices': [
                'Back',
                'PyPass (unencrypted)'
            ]
        },
        {'type': 'input', 'when': lambda _: _['main'] == 'Export data' and _['export'] != 'Back', 'message': 'Export '
                                                                                                             'file '
                                                                                                             'name?',
         'name': 'export_filepath'},
        {
            'message': 'Enter the filepath to upload:',
            'type': 'filepath',
            'when': lambda _: _['main'] == 'Import data' and _['import'] != 'Back',
            'name': 'filepath',
            'validate': PathValidator(),
            'only_files': True
        },
        {
            'message': 'What would you like to do?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Settings',
            'name': 'settings',
            'choices': [
                'Back',
                'Manage folders',
                'Change password'
            ]
        }
    ]
    return inquirer(var)


def simple_choice_menu(choices):
    var = [
        {
            'message': 'What would you like to do?',
            'type': 'list',
            'choices': choices
        }
    ]
    return inquirer(var)[0]


def confirm_choice(title: str):
    var = [{
        'message': title,
        'type': 'list',
        'choices': [
            'No',
            'Yes'
        ]
    }]
    return inquirer(var)[0]


def inquirer(questions):
    try:
        result = prompt(questions, vi_mode=True)
        return result
    except InvalidArgument:
        print('No available choices')
