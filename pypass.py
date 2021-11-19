import json
import pyperclip
import os.path
import uuid

from getpass import getpass
from InquirerPy.utils import color_print
from src import CLI
from src import data_manager


def selectItem(items):
    items = [[x["UUID"], x["name"]] for x in items]
    items.insert(0, 'Back')
    select = [
        {
            'type': 'list',
            'message': 'What would you like to do?',
            'choices': items
        },
    ]
    selected_item = CLI.prompt(select)[0]
    if selected_item == 'Back':
        return None
    else:
        return selected_item[0]


def getItem(items):
    UUID = selectItem(items)
    if UUID is not None:
        for x in items:
            if x["UUID"] == UUID:
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


def delItem(items):
    UUID = selectItem(items)
    if UUID is not None:
        for x in items:
            if x["UUID"] == UUID:
                items.remove(x)
                break


def createItem(result):
    item = {"name": result["loginName"],
            "username": result["loginUsername"],
            "uri": result["loginURI"],
            "password": getpass("Password:"),
            "UUID": str(uuid.uuid4())}
    return item


def importItems(result):
    option = result['import']
    filepath = result['filepath']
    items = []
    if option == 'Bitwarden (unencrypted)':
        data = json.load(open(filepath, 'r'))['items']
        for x in data:
            if x['type'] == 1:
                item = {}
                item["name"] = x["name"]
                item["uri"] = x["login"]["uris"][0]["uri"]
                item["username"] = x["login"]["username"]
                item["password"] = x["login"]["password"]
                item["UUID"] = x["id"]
                items.append(item)
    return items



def initDataFile(init_data_file):
    init_crypto = data_manager.Crypto()
    match = False
    while not match:
        match = init_crypto.password_comp(getpass('password please:'),
                                          getpass('confirm password please:'))

        if match:
            color_print([(CLI.CLI.get_colour(CLI.CLI(), "Success"), 'Password updated.')])

        else:
            color_print([(CLI.CLI.get_colour(CLI.CLI(), "Alert"), 'Passwords do not match!')])

    init_data_file.save(init_data_file.filepath, init_crypto, '{"config":[],"items":[]}')

if __name__ == '__main__':
    crypto = data_manager.Crypto()
    data_file = data_manager.FileData()
    init_result = CLI.first_menu()

    if init_result["init"] == 'Exit':
        exit()
    elif init_result["upload"] is not None:
        data_file.filepath = init_result["upload"]
    elif init_result["create"] is not None:
        if init_result["create"] != '':
            data_file.filepath = init_result["create"]
        if os.path.exists(data_file.filepath.__str__()):
            color_print([(CLI.CLI.get_colour(CLI.CLI(), "Warning"), 'File already exists! Selecting this file.')])
        else:
            initDataFile(data_file.filepath)  # TODO this needs fixed # what was it repesenting

    data_manager.load(crypto)

    try:
        json_data = json.loads(data_file.content) #<-- Fixed this
    except None:
        color_print([(CLI.CLI.get_colour(CLI.CLI(), "Alert"), 'Incorrect password!')])
    finally:
        exit()

    while True:
        main_result = CLI.second_menu()
        option = main_result["main"]
        if option == 'Exit':
            if main_result["save"] != 'Cancel':
                if main_result["save"] == 'Yes':
                    data_manager.save(json_data)  # TODO this needs fixed
                exit()
        elif option == 'Get login':
            getItem(json_data["items"])
        elif option == 'Add login':
            if main_result['loginName'] == '':
                print('Name required!')
            elif main_result['loginUsername'] == '':
                print('Username required!')
            else:
                json_data["items"].append(createItem(main_result))
        elif option == 'Del login':
            delItem(json_data["items"])
        elif option == 'Import data' and main_result["import"] != 'Back':
            json_data["items"].extend(importItems(main_result))
