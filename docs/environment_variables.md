#Setting Up the .env File
SerialBox uses the python-dotenv package to maintain a file that includes
a list of specific environment variables that are used by both it's Django 
settings module and it's Dockerfile.  python-dotenv evaluates a file named
`.env` within your SerialBox root directory and uses those values to connect
to a Djago database backend (postgresql by default).

1. Create a .env File in your SerialBox root directory
2. Add the following environment values:

Environment Variable    |   Description
--------------------    |   --------
SERIALBOX_USER          |   The SerialBox database user.
SERIALBOX_PASSWORD      |   The SerialBox database user's password.
SERIALBOX_DB            |   The name of the SerialBox database.
SERIALBOX_DB_HOST       |   The host of the database (not required- default is localhost)
SERIALBOX_DB_PORT       |   The port of the database (not required- default is 5432)

For example:

    SERIALBOX_USER=myuser
    SERIALBOX_PASSWORD=verysecurepassword
    SERIALBOX_DB=serialbox
    SERIALBOX_DB_HOST=db.host.xyz
    SERIALBOX_DB_PORT=5432