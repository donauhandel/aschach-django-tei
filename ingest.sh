# composer require acdh-oeaw/arche-ingest
python manage.py arche
vendor/bin/arche-import-metadata ./media/tei_out/arche.ttl http://127.0.0.1/api username password --retriesOnConflict 25