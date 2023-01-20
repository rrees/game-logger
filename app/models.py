from collections import namedtuple

GameLog = namedtuple(
    "GameLog",
    [
        "id",
        "name",
        "system",
        "date_played",
        "tags",
        "notes",
    ],
)
