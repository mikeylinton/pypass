from InquirerPy import prompt
from InquirerPy.validator import PathValidator
from Data import *
class CLI:
    def __init__(self):
        self.initQuestions = [
        {
            'message': 'Default file not found! What would you like to do?',
            'type': 'list',
            'when': lambda _: not fileExists(Data().filepath),
            'choices': [
                'Select existing file',
                'Create new file',
                'Exit'
            ],
            'name': 'init'
        },
        {
            'message': 'Enter the filepath to upload:',
            'type': 'filepath',
            'when': lambda _: _['init'] == 'Select existing file',
            'validate': PathValidator(),
            'only_files': True,
            'name': 'filepath'
        },
        {
            'message': 'Enter the file name, press return to use default:', 
            'type': 'input', 
            'when': lambda _: _['init'] == 'Create new file',
            'name': 'filepath'
        }
        ]
        self.mainQuestions = [
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
        # {
        #     'message': 'What would you like to do?',
        #     'type': 'list',
        #     'when': lambda _: _['main'] == 'Settings',
        #     'choices': [
        #         'Change Password',
        #         'Back'
        #     ],
        #     'name': 'settings'
        # },
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Entry name?', 'name': 'loginName'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'URI?', 'name': 'loginURI'},
        {'type': 'input', 'when': lambda _: _['main'] == 'Add login', 'message': 'Username?', 'name': 'loginUsername'},
        ]

def inquirer(questions):
    try:
        result = prompt(questions, vi_mode=True)
        return result
    except InvalidArgument:
        print('No available choices')
