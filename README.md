# Filmstore - API
An API to access an SQLite DB on a raspberry that manages my film rolls so i can find the photos i took.


## POST REQUESTS
/films
*creates a film*
```json
{
  "name": "Kodak Gold",
  "iso": 200,
  "development_info": "Many details go here",
  "type": 1
}
```

/pictures
```json
{
  "description": "",
  "location": "",
  "aperture": "",
  "shutter_speed": "",
  "posted": true,
  "printed": false
}
```

/filmrolls
```json
{
  "camera": "Olympus OM2n",
  "film": 123,
  "identifier": "OM2-1",
  "pictures": [123, 124, 125, 126],
  "status": 4
}
```
