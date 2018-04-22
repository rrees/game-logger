from collections import namedtuple

GameLog = namedtuple('GameLog',
    [
        'id',
        'name',
        'date_played',
        'tags',
        'notes',
    ])