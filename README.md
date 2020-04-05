# eldiario

**eldiario** is a command-line utility to write down notes, in the form of a journal. eldiario-cli is written in Python.

## Installation

The client application is written in Python and is uses requests.
Here you'll be spending most of the time.

## Usage

When you launch eldiario, you are put inside your choice of editor (eldiario reads `$EDITOR`).

You can pass date-time in the format of YYMMDDHHMMSS to override the `--new` timestamp.
Passing full DateTime helps in sorting.

<!-- ## Configuration -->

## Development

With each diary entry, there goes some metadata which are:

- Datetime: This differentiates one entry from another.
- Author: To show only the entries written by the current user.
- Body: The actual entry.
- UUID: Random generated UUID at the front end

### Test API

For testing following curl commands can be used.

Add a new entry:

    curl -X POST -H "Content-Type: application/json" \
    -d '{"id": "bd7b69fa-9207-4996-91cd-b7eec3fce21b", \
    "body": "Starting days with eldiario",\
    "datetime": "20190729224822",\
    "author": "sntshk"}' http://localhost:8080/entry

Get all entries:

    curl -H "Content-Type: application/json" http://localhost:8080/entry

Get a specific entry:

    curl -H "Content-Type: application/json" \
    http://localhost:8080/entry/bd7b69fa-9207-4996-91cd-b7eec3fce21b

Update entry:

    curl -X PUT -H "Content-Type: application/json" \
    -d '{"id": "bd7b69fa-9207-4996-91cd-b7eec3fce21b", body": "eldiario is cool!", \
    "datetime": "20190729224822", "author": "sntshk"}' \
    http://localhost:8080/entry/bd7b69fa-9207-4996-91cd-b7eec3fce21b

Delete a entry:

    curl -X DELETE -H "Content-Type: application/json" \
    http://localhost:8080/entry/bd7b69fa-9207-4996-91cd-b7eec3fce21b
