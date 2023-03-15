# composer require acdh-oeaw/arche-ingest
ARCHE=http://127.0.0.1/api
PROJECT_NAME=donauhandel-aschach

python manage.py arche
vendor/bin/arche-import-metadata ./media/tei_out/arche.ttl ${ARCHE} username password --retriesOnConflict 25
# vendor/bin/arche-import-binary ./to_ingest https://id.acdh.oeaw.ac.at/${PROJECT_NAME} http://127.0.0.1/api username password --skip not_exist