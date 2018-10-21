CREDENTIALSCHEMA = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "fromaddr": {"type": "string"},
        "password": {"type": "string"}
    },
    "additionalProperties": False,
    "required": ["fromaddr", "password"]
}
