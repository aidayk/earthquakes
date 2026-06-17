# Italian Earthquake Query Project

This project was developed for the Lab of Software Project Development course.

The program queries recent earthquake data in Italy using the INGV API, stores the results in a local SQLite database, and returns the strongest earthquakes according to user-defined command-line arguments.

Team members:

* Aiday Karazhan
* Osman Sokolov

## Main features

The project implements the required features from the project manual:

* Git and GitHub workflow with issues, branches, commits and pull requests
* Standard Python package structure
* Command-line interface with `argparse`
* CSV file handling with the `csv` module
* Italian geographic bounding box stored in `bounding_box.csv`
* Earthquake data gathering from the INGV API
* Local SQLite database using `sqlite3`
* Querying and printing the strongest earthquakes
* Unit tests using Python `unittest`

## Project structure

```text
earthquakes/
│
├── README.md
├── LICENSE
├── test_project.py
├── earthquakes.db
│
└── earthq_package/
    ├── __init__.py
    ├── main.py
    ├── earthquakes.py
    ├── database.py
    ├── query.py
    ├── write_bounding_box.py
    └── bounding_box.csv
```

Some file names may differ slightly depending on the final implementation, but the main logic is organized inside the `earthq_package` package.

## Installation

Before running the project, install the required external dependency:

```bash
pip install -r requirements.txt
```

The project uses `requests` to query the INGV API. Other modules used in the project, such as `argparse`, `csv`, `sqlite3`, and `unittest`, are part of the Python standard library.


## How to run the program

From the root folder of the project, run:

```bash
python -m earthq_package.main --days 30 --K 5 --magnitude 2.0
```

Example meaning:

```text
--days 30
```

queries earthquakes from the last 30 days.

```text
--K 5
```

returns at most 5 earthquakes.

```text
--magnitude 2.0
```

returns only earthquakes with magnitude at least 2.0.

The output is a list of earthquakes sorted by decreasing magnitude.



## Add-on

If the add-on is enabled in the final version, it can be run with:

```bash
python -m earthq_package.main --days 30 --K 3 --magnitude 3.0 --addon
```

The add-on extends the basic output with additional information about nearby municipalities.

## How to create the bounding box CSV

The Italian bounding box can be generated with:

```bash
python -m earthq_package.write_bounding_box
```

This creates or updates `bounding_box.csv` with the coordinates used to restrict the earthquake query to Italy.

## How to create the SQLite database manually

If needed, the database can be created manually with:

```bash
python -c "from earthq_package.database import create_earthquake_db; create_earthquake_db(30)"
```

This creates and populates `earthquakes.db` using earthquake data from the last 30 days.

## How to run the tests

Run the test suite from the root folder:

```bash
python -m unittest test_project -v
```

The tests check that:

* Padova, Palermo and Parma are inside the Italian bounding box
* no earthquake in the database has magnitude greater than 9.5
* query results are sorted by decreasing magnitude
* the database does not contain null magnitude values

## Implemented project steps

1. The repository was forked and managed through GitHub.
2. The project was organized as a Python package.
3. Command-line arguments were added with `argparse`.
4. The Italian bounding box was stored and read using the `csv` module.
5. Earthquake data was gathered from the INGV API.
6. Earthquake data was stored in a local SQLite database.
7. The database was queried to return the strongest earthquakes matching the user input.
8. A `unittest` test suite was added.
9. An optional add-on was implemented if enabled through the command line.

## Notes

The project uses live data from the INGV API. Therefore, the exact output may change depending on when the program is executed.
