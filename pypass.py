import json
import pyperclip
import os.path
import uuid

from getpass import getpass
from InquirerPy.utils import color_print
from cryptography.fernet import InvalidToken

from src import CLI
from src import data_manager


def get_item_uuid(items):
    if not items:
        color_print([(CLI.get_colour("Warning"), 'No saved logins!')])
        return None
    else:
        items_uuid_name = [[x["UUID"], x["name"]] for x in items]
        # noinspection PyTypeChecker
        items_uuid_name.insert(0, 'Back')
        selected_item = CLI.simple_choice_menu(items_uuid_name)
        if selected_item == 'Back':
            return None
        else:
            return selected_item[0]


def get_username_password(items, item_uuid):
    for item in items:
        if item["UUID"] == item_uuid:
            username = item["username"]
            password = item["password"]
            if username is not None:
                pyperclip.copy(username)
                print('Username: ' + username)
                input('Username saved to clipboard, press return to get password.')
            if password is not None:
                pyperclip.copy(password)
                input('Password saved to clipboard, press return to clear clipboard.')
            break


def del_item(items, item_uuid):
    for item in items:
        if item["UUID"] == item_uuid:
            items.remove(item)
            break


def create_item(result):
    item = {"name": result["loginName"],
            "username": result["loginUsername"],
            "uri": result["loginURI"],
            "password": getpass("Password:"),
            "UUID": uuid.uuid4().__str__()}
    return item


def import_items(result):
    import_option = result["import"]
    filepath = result["filepath"]
    items = []
    if import_option == 'Bitwarden (unencrypted)':
        import_data = json.load(open(filepath, 'r'))["items"]
        for x in import_data:
            if x["type"] == 1:
                try:
                    uri = x["login"]["uris"][0]["uri"]
                except KeyError:
                    uri = None
                try:
                    username = x["login"]["username"]
                except KeyError:
                    username = None
                try:
                    password = x["login"]["password"]
                except KeyError:
                    password = None
                import_item = {"name": x["name"], "uri": uri,
                               "username": username,
                               "password": password, "UUID": x["id"]}
                items.append(import_item)
    return items


def update_password(update_crypto):
    match = False
    while not match:
        match = update_crypto.password_match(getpass('Password:'),
                                             getpass('confirm password:'))

        if match:
            color_print([(CLI.get_colour('Success'), 'Password updated.')])

        else:
            color_print([(CLI.get_colour('Alert'), 'Passwords do not match!')])


def init_data_file(filepath):
    init_crypto = data_manager.Crypto()
    update_password(init_crypto)
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
                color_print([(CLI.get_colour('Warning'), 'File already exists! Selecting this file.')])
            else:
                init_data_file(data.filepath)

    crypto.key = getpass('Password:')
    try:
        data_manager.load(crypto, data)
    except InvalidToken:
        color_print([(CLI.get_colour('Alert'), 'Invalid file or incorrect password!')])
        exit()
    json_data = None
    try:
        json_data = json.loads(data.content)
    except TypeError as e:
        color_print([(CLI.get_colour('Alert'), e.__str__().capitalize() + '.')])
        exit()

    while True:
        main_result = CLI.second_menu()
        option = main_result["main"]
        if option == 'Exit':
            if main_result["save"] != 'Cancel':
                if main_result["save"] == 'Yes' and json_data is not None:
                    data_manager.save(crypto, data.filepath, json_data)
                exit()
        elif option == 'Get login' or option == 'Del login':
            item_uuid_result = get_item_uuid(json_data["items"])
            if item_uuid_result is not None:
                if option == 'Get login':
                    get_username_password(json_data["items"], item_uuid_result)
                else:
                    confirm_choice_result = CLI.confirm_choice(
                        'Are you sure you want to delete ' + item_uuid_result + '?')
                    if confirm_choice_result == 'Yes':
                        del_item(json_data["items"], item_uuid_result)
        elif option == 'Add login':
            if main_result["login_name"] == '':
                print('Name required!')
            elif main_result["login_username"] == '':
                print('Username required!')
            else:
                new_item = create_item(main_result)
                json_data["items"].append(new_item)
        elif option == 'Import data' and main_result["import"] != 'Back':
            json_data["items"].extend(import_items(main_result))
        elif option == 'Settings':
            if main_result["settings"] == 'Change password':
                if data_manager.key_match(crypto.key, getpass('Current password:')):
                    color_print([(CLI.get_colour('Success'), 'Correct password.')])
                    update_password(crypto)
                else:
                    color_print([(CLI.get_colour('Alert'), 'Password incorrect!')])

