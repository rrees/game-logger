from collections import namedtuple

GameLog = namedtuple('GameLog',
    [
        'id',
        'name',
        'log_date',
        'tags',
        'notes',
    ])