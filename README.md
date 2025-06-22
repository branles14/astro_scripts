Some small scripts that use the [Astral](https://astral.readthedocs.io/) library.

Location data is resolved via `location.get_location()` which checks
command-line arguments first and falls back to environment variables or
configuration files. If running under Termux and `termux-location` is
available, that tool is used as a last resort to retrieve coordinates. The
timezone is automatically determined from the resolved coordinates using the
`timezonefinder` library, so only latitude and longitude need to be provided.
