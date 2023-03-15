# composer require acdh-oeaw/arche-ingest
python manage.py arche
vendor/bin/arche-import-metadata ./media/tei_out/arche.ttl http://127.0.0.1/api username password --retriesOnConflict 25

vendor/bin/arche-import-binary ./to_ingest https://id.acdh.oeaw.ac.at/donauhandel-aschach http://127.0.0.1/api username password --skip not_exist