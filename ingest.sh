# composer require acdh-oeaw/arche-ingest
# ARCHE=http://127.0.0.1/api
ARCHE="https://arche-curation.acdh-dev.oeaw.ac.at/api"
PROJECT_NAME=donauhandel-aschach
ARCHE_LOGIN="${ARCHE_LOGIN:=username}"
ARCHE_PASSWORD="${ARCHE_PASSWORD:=password}"


# python manage.py arche
# vendor/bin/arche-import-metadata ./media/tei_out/arche.ttl ${ARCHE} ${ARCHE_LOGIN} ${ARCHE_PASSWORD} --retriesOnConflict 25
# vendor/bin/arche-import-binary ./to_ingest https://id.acdh.oeaw.ac.at/${PROJECT_NAME} ${ARCHE} ${ARCHE_LOGIN} ${ARCHE_PASSWORD} --skip not_exist
#  vendor/bin/arche-delete-resource https://id.acdh.oeaw.ac.at/donauhandel-aschach/DepHarr_H026.xml  ${ARCHE} ${ARCHE_LOGIN} ${ARCHE_PASSWORD}