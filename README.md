# The Toll Registers of Aschach (1706-1740): Database and Analysis

## Data conversion repo

* Repo for converting data from the FWF funded project "The Toll Registers of Aschach (1706-1740): Database and Analysis" into XML/TEI and ARCHE-RDF.
* The main part of the code and the data were written in spring 2021. Completion was delayed due to COVID and related data curation.


## install

* clone the repo
* (create a virtual environment)
* install needed Python packages `pip install -r requirments_dev.txt`. 
* set up a postgres database `aschach` and read in the (ToDo:) db-dump
* provide required db-credentials as environment variables (see `djangobaseproject/settings.py`)
* run `python manage.py startserver`.