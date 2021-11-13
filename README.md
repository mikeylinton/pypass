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
            "password":"gAAAAABhj8Bhqz_Q4b-cGp9z-FKW8soLHQ4j30LtMxIz1MyyVGjIAbh7b4Gqnjwm-pOC8FFVu8FwpGie4u8YXGumZG1asWXieA==", 
            "uri":"https://www.example.com/"
        }
    ]
}
```