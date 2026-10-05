# Provenance and publication changes

## Academic source

This repository is based on Enrique Vicente Pujante's uploaded `ProyectoRedesDatos.zip`, containing the server/client coursework and explanatory reports. The archive contains no Git history, so no original commit history or historical contribution dates can be preserved. No code was copied from another student's repository.

## Selection

Retained as the main deliverable:

- `EnriqueVicentePujante_servidorP3.py` → `server.py`.
- `EnriqueVicentePujante_servidor_clienteP3.py` → `client.py`.

Excluded from this curated distribution:

- Earlier standalone REST client: overlaps with the final project and contains a temperature-average precedence error and comparisons between precipitation probability and observed rainfall.
- Original screenshots: redundant desktop captures, some with misleading unit labels or results from the earlier client.
- Two substantially overlapping server reports and the earlier client report: useful source context, replaced here with focused Markdown documentation.
- `cuestion_servidor.txt`: working notes and assignment material, not application documentation.

The original upload remains separate and unchanged.

## Publication preparation

The following changes were prepared with AI assistance after the academic work:

- Descriptive filenames, English README and API documentation.
- Embedded AEMET credential replaced with server-side `AEMET_API_KEY`.
- Removed the client's unused placeholder `api_key` query argument.
- Added parameter validation, network timeouts and upstream error responses.
- Disabled Flask debug mode and added dependency/configuration files.
- Clarified precipitation-probability labels in the client.
- Added offline regression tests with synthetic data.

The original forecast and historical transformation functions remain substantially unchanged. Scientific interpretation issues are documented explicitly; this preparation does not claim to have fixed or live-validated them. Original source comments and console interaction remain in Spanish.

## Licensing

The code and original documentation are released under the MIT License at the author's request. Academic authorship is retained. The licence does not cover institutional assignment material, AEMET data or third-party dependencies. Original assignment text is not included.
