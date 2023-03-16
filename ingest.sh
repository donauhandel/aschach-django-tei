# composer require acdh-oeaw/arche-ingest
ARCHE=https://arche-dev.acdh-dev.oeaw.ac.at/api
PROJECT_NAME=donauhandel-aschach
ARCHE_LOGIN="${ARCHE_LOGIN:=username}"
ARCHE_PASSWORD="${ARCHE_PASSWORD:=password}"


python manage.py arche
vendor/bin/arche-import-metadata ./to_ingest/arche.ttl ${ARCHE} ${ARCHE_LOGIN} ${ARCHE_PASSWORD} --retriesOnConflict 25
# vendor/bin/arche-import-binary ./to_ingest https://id.acdh.oeaw.ac.at/${PROJECT_NAME} ${ARCHE} ${ARCHE_LOGIN} ${ARCHE_PASSWORD} --skip not_exist