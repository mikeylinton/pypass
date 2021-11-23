import json
import pyperclip
import os.path
import uuid

from getpass import getpass
from InquirerPy.utils import color_print
from cryptography.fernet import InvalidToken

from src import CLI
from src import data_manager


def select_item(items):
    items_uuid_name = [[x["UUID"], x["name"]].__str__() for x in items]
    items_uuid_name.insert(0, 'Back')
    select = [
        {
            'type': 'list',
            'message': 'What would you like to do?',
            'choices': items_uuid_name
        },
    ]
    selected_item = CLI.prompt(select)[0]
    if selected_item == 'Back':
        return None
    else:
        return selected_item[0]


def get_item(items):
    if not items:
        color_print([(CLI.CLI.get_colour(CLI.CLI(), "Warning"), 'No saved logins!')])
    else:
        items_uuid = select_item(items)
        if items_uuid is not None:
            for x in items:
                if x["UUID"] == items_uuid:
                    username = x["username"]
                    password = x["password"]
                    if username is not None:
                        pyperclip.copy(username)
                        print('Username: ' + username)
                        input('Username saved to clipboard, press return to get password.')
                    if password is not None:
                        pyperclip.copy(password)
                        input('Password saved to clipboard, press return to clear clipboard.')
                    break


def del_item(items):
    item_uuid = select_item(items)
    if item_uuid is not None:
        for x in items:
            if x["UUID"] == item_uuid:
                items.remove(x)
                break


def create_item(result):
    new_item = {"name": result["loginName"],
                "username": result["loginUsername"],
                "uri": result["loginURI"],
                "password": getpass("Password:"),
                "UUID": uuid.uuid4().__str__()}
    return new_item


def import_items(result):
    import_option = result['import']
    filepath = result['filepath']
    items = []
    if import_option == 'Bitwarden (unencrypted)':
        import_data = json.load(open(filepath, 'r'))['items']
        for x in import_data:
            if x['type'] == 1:
                import_item = {"name": x["name"], "uri": x["login"]["uris"][0]["uri"],
                               "username": x["login"]["username"],
                               "password": x["login"]["password"], "UUID": x["id"]}
                items.append(import_item)
    return items


def init_data_file(filepath):
    init_crypto = data_manager.Crypto()
    match = False
    while not match:
        match = init_crypto.password_comp(getpass('Password:'),
                                          getpass('confirm password:'))

        if match:
            color_print([(CLI.CLI.get_colour(CLI.CLI(), "Success"), 'Password updated.')])

        else:
            color_print([(CLI.CLI.get_colour(CLI.CLI(), "Alert"), 'Passwords do not match!')])

    data_manager.save(init_crypto, filepath, json.loads('{"config":[],"items":[]}'))


if __name__ == '__main__':
    crypto = data_manager.Crypto()
    data = data_manager.FileData()
    while not data_manager.file_exists(data.filepath):
        init_result = CLI.first_menu()
        if init_result["init"] == 'Exit':
            exit()
        elif init_result["upload"] is not None and init_result["upload"] != '':
            data.filepath = init_result["upload"]
        elif init_result["create"] is not None:
            if init_result["create"] != '':
                data.filepath = init_result["create"]
            if os.path.exists(data.filepath.__str__()):
                color_print([(CLI.CLI.get_colour(CLI.CLI(), "Warning"), 'File already exists! Selecting this file.')])
            else:
                init_data_file(data.filepath)

    crypto.key = getpass('Password:')
    try:
        data_manager.load(crypto, data)
    except InvalidToken:
        color_print([(CLI.CLI.get_colour(CLI.CLI(), "Alert"), 'Invalid file or incorrect password!')])
        exit()
    json_data = None
    try:
        json_data = json.loads(data.content)
    except TypeError as e:
        color_print([(CLI.CLI.get_colour(CLI.CLI(), "Alert"), e.__str__().capitalize() + '.')])
        exit()

    while True:
        main_result = CLI.second_menu()
        option = main_result["main"]
        if option == 'Exit':
            if main_result["save"] != 'Cancel':
                if main_result["save"] == 'Yes' and json_data is not None:
                    data_manager.save(crypto, data.filepath, json_data)
                exit()
        elif option == 'Get login':
            get_item(json_data["items"])
        elif option == 'Add login':
            if main_result['loginName'] == '':
                print('Name required!')
            elif main_result['loginUsername'] == '':
                print('Username required!')
            else:
                item = create_item(main_result)
                json_data["items"].append(item)
        elif option == 'Del login':
            del_item(json_data["items"])
        elif option == 'Import data' and main_result["import"] != 'Back':
            json_data["items"].extend(import_items(main_result))
