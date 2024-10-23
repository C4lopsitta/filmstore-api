# Filmstore - API
An API to access an SQLite DB on a raspberry that manages my film rolls so i can find the photos i took.

## Planned features
- [ ] Option to skip image processing
- [x] Option to store original size images
- [x] Folder settings for storing original sized images and thumbnails
- [ ] Negative processing settings
- [X] User authentication with multiple user accounts
> [!Note]
> While technically supported by the DB, right now no authentication is enforced as the API is broken and needs to be 
> updated to use the new DB functions.
- [X] Film stock grouping (to group multiple versions of the same stock, like a group for Kodak Portra that contains all the ISOs and formats)
- [X] Projects to group images or rolls
- [X] Non-film images to allow for general image backups
- [X] Image albums
- [X] Docker container

> [!Note]
> Currently the API endpoints have changed *quite a bit* so the app is broken. Right now the API is my priority and I'll 
> get back to the App as soon as the API has reached a good state.

> [!Note]
> The database schema has been completely redone [as shown in the diagram here](Db/README.md) and the old one was not 
> migrated. Data will be lost, no intentions on making a migration as the schema has changed a lot and i kinda figured 
> no one else but me will care.

## Running the API
You can run the Docker container by simply building and launching the included `Dockerfile`:.
```bash
docker build . -t "filmstore"
docker run -d "filmstore"
```
A running script, which expects to have a python VENV available in the `venv` folder, is also available.
You can run in with:
```bash
./filmstore.sh
```
If automated running on boot is needed, you can create a user systemd service.
```
[Unit]
Description=Filmstore DB API
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/PATH-TO-FILMSTORE/filmstore/filmstore.sh
Restart=always
RestartSec=12

[Install]
WantedBy=default.target
```
Additionally, an Avahi mDNS discovery service is available, you can install it through the `scripts/discovery_service_create.sh` 
script. This script will automatically install the needed packages (`avahi-daemon` and `avahi-utils`) and copy the config 
file `config/filmstore_discovery.service` into the Avahi configuration folder, lastly it will enable and start the mDNS 
Avahi service.

## Requirements
Some additional software is needed to compress the pictures properly:
- ImageMagik
- DCRAW
On a Debian/Ubuntu system these can be installed with:
```bash
apt-get install imagemagik dcraw
```
You can make do without these but image upload won't be supported. Plans on adding an option to skip image processing 
exist but are not a priority as of today.

## API Documentation
Multiple endpoints are available.

### GET /api/v1
Returns a JSON with 200

### GET /api/v1/films
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
      "type": 1,
      "format": 1
    }
  ]
}
```

### GET /api/v1/films/{id}
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
    "type": 1,
    "format": 1
  }
}
```

### GET /api/v1/filmrolls
Returns all the film rolls stored.
Response:
```json
{
  "status": 200,
  "message": "",
  "filmrolls": [
    {
      "film": {
        "id": 123,
        "name": "Ilford HP5+",
        "ISO": 400,
        "development_info": "",
        "type": 1,
        "format": 1
      },
      "pictures": [123, 124, 125],
      "status": 3,
      "camera": "Olympus OM2n",
      "identifier": "Archival Identifier",
      "db_id": 123
    }
  ]
}
```

### GET /api/v1/filmrolls/{id}
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
    "type": 1,
    "format": 1
  },
  "pictures": [123, 124, 125],
  "filmroll_status": 3,
  "camera": "Olympus OM2n",
  "identifier": "Archival Identifier"
}
```

### GET /api/v1/pictures/{id}
Returns a single image details with the image encoded in Base64 in JPEG format.
Response:
```json
to be defined
```

### POST /api/v1/films
Adds a new film brand.
Request:
```json
{
  "name": "Lomography Berlin Kino",
  "iso": 400,
  "development_info": "ISO 100 pull gives a thick grain",
  "type": 1,
  "format": 1
}
```
Response:
```json
{
  "status": 200,
  "message": ""
}
```

### POST /api/v1/films/{id}
Alters a film stock with the given data.
Request:
```json
{
  "name": "Lomography Berlin Kino",
  "iso": 400,
  "development_info": "ISO 100 pull gives a thick grain",
  "type": 1,
  "format": 1 
}
```
Response:
```json
{
  "status": 200,
  "message": "Film roll {id} has been updated successfully"
}
```

### POST /api/v1/pictures
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

### POST /api/v1/filmrolls
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
Response:
```json
{
  "status": 200,
  "message": "",
  "filmroll_id": 123
}
```

### DELETE /api/v1/films/{id}
Deletes permanently the specified film ID. Do note that any film roll referencing the stock to delete will also be 
permanently deleted with no way of recovering them. This means that any picture in those film rolls will also be removed.
Response:
```json
{
  "status": 200,
  "message": "Film stock deleted successfully",
  "deleted_item": {
    "name": "Lomography Berlin Kino",
    "iso": 400,
    "development_info": "ISO 100 pull gives a thick grain",
    "type": 1,
    "format": 1 
  }
}
```

## Enumeration definitions
A value of 0 is always to be considered `undefined`.
### Film Format (format)
1. 35mm
2. 120
3. 127
4. 110
5. Sheet film

### Film Type (type)
1. Black and White Panchromatic
2. Black and White Orthochromatic
3. Color
4. Infrared

### Development Status (filmroll_status)
1. In camera
2. To be developed
3. Developed
4. Scanned
5. Archived
