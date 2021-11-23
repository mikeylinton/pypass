import os.path

from InquirerPy import prompt
from InquirerPy.exceptions import InvalidArgument
from InquirerPy.validator import PathValidator

from src import data_manager


class CLI:
    def __init__(self):
        self.colour = {
            "Alert": "#dc3545",
            "Success": "#198754",
            "Warning": "#ffc107"
        }

    def get_colour(self, colour: str):
        return self.colour[colour]


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
                # 'Settings',
                'Exit'
            ],
            'name': 'main'
        },
        {
            'message': 'Would you like to save?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Exit',
            'choices': [
                'Cancel',
                'No',
                'Yes'
            ],
            'name': 'save'
        },
        {
            'message': 'Import from?',
            'type': 'list',
            'when': lambda _: _['main'] == 'Import data',
            'name': 'import',
            'choices': [
                'Bitwarden (unencrypted)',
                'Back'
            ]
        },
        {
            'message': 'Enter the filepath to upload:',
            'type': 'filepath',
            'when': lambda _: _['main'] == 'Import data' and _['import'] != 'Back',
            'name': 'filepath',
            'validate': PathValidator(),
            'only_files': True
        },
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Entry name?',
         'name': 'loginName'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login' and _['loginName'] != '', 'message': 'URI?',
         'name': 'loginURI'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login' and _['loginName'] != '',
         'message': 'Username?', 'name': 'loginUsername'},
    ]
    return inquirer(var)


def inquirer(questions):
    try:
        result = prompt(questions, vi_mode=True)
        return result
    except InvalidArgument:
        print('No available choices')
