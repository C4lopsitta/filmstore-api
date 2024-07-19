# Filmstore - API
An API to access an SQLite DB on a raspberry that manages my film rolls so i can find the photos i took.

## API Documentation
Multiple endpoints are available.

### GET /
Returns a JSON with 200

### GET /films
Returns a list of all Films (as in brands)
Response:
```json
{
  "status": 200,
  "message": "",
  "films": [
    {
      "id": 123,
      "name": "Ilford HP5+",
      "ISO": 400,
      "development_info": "",
      "type": 1
    }
  ]
}
```

### GET /films/{id}
Returns a single film (as in brand)
Response:
```json

{
  "status": 200,
  "message": "",
  "films": {
    "id": 123,
    "name": "Ilford HP5+",
    "ISO": 400,
    "development_info": "",
    "type": 1
  }
}
```

### GET /filmrolls
Returns all the film rolls stored.
Response:
```json
{
  "to be defined": ""
}
```

### GET /filmrolls/{id}
Returns a single film roll
Response:
```json
{
  "status": 200,
  "message": "",
  "id": 123,
  "film": {
    "id": 123,
    "name": "Ilford HP5+",
    "ISO": 400,
    "development_info": "",
    "type": 1
  },
  "pictures": [123, 124, 125],
  "filmroll_status": 3,
  "camera": "Olympus OM2n",
  "identifier": "Archival Identifier"
}
```

### GET /pictures/{id}
Returns a single image details with the image encoded in Base64 in JPEG format.
Response:
```json
to be defined
```

### POST /films
Adds a new film brand.
Request:
```json
{
  "name": "Lomography Berlin Kino",
  "iso": 400,
  "development_info": "ISO 100 pull gives a thick grain",
  "type": 1
}
```
Response:
```json
{
  "status": 200,
  "message": "",
  "request_json": "json of request"
}
```

### POST /pictures
Adds a new image with details.
HTTP Form Request:
- file: contains image file (currently only `image/jpeg` is supported)
- req: contains json formatted as follows
Request:
```json
{
  "description": "",
  "location": "",
  "aperture": "1.4",
  "shutter_speed": "1/1000",
  "posted": false,
  "printed": false
}
```
Response:
```json
{
  "status": 200,
  "message": "",
  "picture_id": 123
}
```

### POST /filmrolls
Adds a new film roll.
Request:
```json
{
  "camera": "Olympus Pen EE",
  "film": 123,
  "identifier": "Archival identifier",
  "pictures": [123, 124, 125],
  "status": 5
}
```
