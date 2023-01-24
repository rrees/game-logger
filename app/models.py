from collections import namedtuple

GameLog = namedtuple(
    "GameLog",
    [
        "id",
        "game_name",
        "system",
        "date_played",
        "tags",
        "notes",
    ],
)
