# PyPass

A lightweight cross-platform password manager using JSON and AES-128 encryption.

Please note: Both the master password and salt are the same, this will be altered in future implementations.

## JSON file structure
```json
{
    //Master password: password
    //Note that whole file is encrypted; passwords may have a second pin for further encryption (TBD)
    "config": [],
    "items":[
        {
            "name":"Exmaple", 
            "username":"Alice", 
            "uri":"https://www.example.com/",
            "password":"password", 
            "UUID":"a8a8a8a8-4b4b-4c4c-4d4d-12e12e12e12e"
        }
    ]
}
```