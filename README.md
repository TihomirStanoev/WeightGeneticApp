# WeightGeneticApp

A prototype web app that compares the real weight and the theoretical weight of a profile.
It then carries the resulting coefficient over to the billet and the finished product.

> **Status:** prototype. The statistics part is not written yet.
> A coefficient pattern was observed in more than 40 measurements.
> All example data in this project is made up.

## Features

- Master data: profiles, workpieces (billets) and references (finished products).
- Extrusion cards that belong to a profile.
- Batches of a reference, with measurements inside each batch.
- Each measurement calculates its own values on save: weight per meter, coefficients against the card and against the theoretical weight, and weight deltas in percent.
- Two roles: `user` can read, `moderator` can also create, edit and delete.
- Small web page: sign in, then browse profiles → workpieces → references, and add a reference.
- Batches, measurements and extrusion cards are not in the web page yet. Use the API or the Django admin.

## Tech stack

- Django 6, Django REST Framework, SimpleJWT
- PostgreSQL
- Vanilla JavaScript (no framework)
- pytest, pytest-django, model-bakery

## Getting started

Not yet checked on a clean machine.

1. Create and activate a virtual environment, then run `pip install -r requirements.txt`.
2. Create a PostgreSQL database.
3. Copy `.env.example` to `.env` and set `SECRET_KEY`, `DEBUG` and `DATABASE_URL`.
4. Run `python manage.py migrate`.
5. Run `python manage.py createsuperuser`.
6. Run `python manage.py runserver` and open `http://127.0.0.1:8000/`.
7. In `/admin/`, set the user's role to `moderator` if you want to create data.

## API overview

All endpoints need a JWT. Reading is allowed for every signed-in user. Writing needs the `moderator` role.
Every list endpoint supports `GET` and `POST`. Every detail endpoint supports `GET`, `PUT`, `PATCH` and `DELETE`.

| Endpoint | Description |
|----------|-------------|
| `POST /api/token/` | Get access and refresh tokens |
| `POST /api/token/refresh/` | Refresh the access token |
| `/api/master-data/profiles/` and `.../<profile_code>/` | Profiles |
| `/api/master-data/profiles/<profile_code>/workpieces/` and `.../<workpiece_material>/` | Workpieces |
| `/api/master-data/profiles/<profile_code>/workpieces/<workpiece_material>/references/` and `.../<reference_material>/` | References |
| `/api/extrusion/profiles/<profile_code>/cards/` and `.../<card_no>/` | Extrusion cards |
| `/api/measurements/references/<reference>/batches/` and `.../<id>/` | Batches |
| `/api/measurements/references/<reference>/batches/<batch_id>/measurements/` and `.../<id>/` | Measurements |

Admin site: `/admin/`.

## Running tests

```bash
pytest
```

There are 57 tests (models, serializers and views). They need the database from `DATABASE_URL`.

## Known issues and next steps

- The statistics part is not written yet.
- The web page stops at references. The next step is references → batches.
- `ALLOWED_HOSTS` is empty, so the project is for local development only.
