# MSHack2020 counting backend

Supports stationary devices which count things.

## Database schema documentation

#### Count

An entitiy with a `count`, `timestamp` and a reference to a `device` and optional free form `data`.

#### Device

An entity with a `id`, `latitude` and `longitude` and optional free form `data`.

`latitude` and `longitude` will be stored with 6 decimal digits precision.

## API documentation

Available at `/docs` of a running instance
