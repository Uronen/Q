FILE = "data.json"
URL = "https://jsonplaceholder.typicode.com/users"

DEFAULT_REPORTS_FOLDER = "REPORTS"

NAME_COLUMN = "name"
FIRSTNAME_COLUMN = "firstname"
LASTNAME_COLUMN = "lastname"

TIMESTAMP_FORMAT = "%Y%m%d%H%M%S"
REPORT_PREFIX = "employees_"


REPORT_COLUMNS = {
    LASTNAME_COLUMN: "sukunimi",
    FIRSTNAME_COLUMN: "etunimi",
    "email": "email",
    "address.street": "katuosoite",
    "address.city": "postitoimipaikka",
    "address.zipcode": "postinumero",
    "phone": "puhelin",
    "website": "nettisivut",
}

TITLES_AND_HONORIFICS = [
    "Mr.",
    "Mrs.",
    "Miss",
    "Dr.",
    "Ms.",
    "Prof.",
    "Rev.",
    "Lady",
    "Sir",
    "Capt.",
    "Major",
    "Lt.-Col.",
    "Col.",
    "Lady",
    "Lt.-Cmdr.",
    "The Hon.",
    "Cmdr.",
    "Flt. Lt.",
    "Brgdr.",
    "Judge",
    "Lord",
    "The Hon. Mrs",
    "Wng. Cmdr.",
    "Group Capt.",
    "Rt. Hon. Lord",
    "Revd. Father",
    "Revd Canon",
    "Maj.-Gen.",
    "Air Cdre.",
    "Viscount",
    "Dame",
    "Rear Admrl.",
]
