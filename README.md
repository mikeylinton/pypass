# PyPass

A lightweight cross-platform password manager using JSON and AES-128 encryption.

Please note: Both the master password and salt are the same, this will be altered in future implementations.

## JSON file structure
```json
{
    "items":[
        {
            "name":"Exmaple", 
            "username":"Alice", 
            "uri":"https://www.example.com/",
            "password":"gAAAAABhj8Bhqz_Q4b-cGp9z-FKW8soLHQ4j30LtMxIz1MyyVGjIAbh7b4Gqnjwm-pOC8FFVu8FwpGie4u8YXGumZG1asWXieA==", 
            "UUID":"a8a8a8a8-4b4b-4c4c-4d4d-12e12e12e12e"
        }
    ]
}
```