# Indian Music Tutor backend

Built with FastAPI.

## Configuration

The database credentials are read from a file specified in env var `DB_CREDENTIALS_JSON`,
with a structure like this:

```json
{
  "user": "my_user",
  "password": "my_password",
  "address": "some.project.mongodb.net",
  "app_name": "IMT0"
}
```

## Environment variables

| name                  | default value          | description                                    |
|-----------------------|------------------------|------------------------------------------------|
| `DB_CREDENTIALS_JSON` | `.db-credentials.json` | file contaning database secrets                |
| `DB_TLS`              | `true`                 | db connection TLS                              |
| `DB_TLS_CA_FILE`      |                        | if set, CA file will be used fro db connection |
| `FRONTEND_URI`        | `http://localhost`     | URI added to CORS allowed origins              |

## Build Docker image

`docker build . -t imt-backend`
