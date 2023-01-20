-- migrate:up

CREATE TABLE IF NOT EXISTS game_logs (
    log_id UUID PRIMARY KEY,
    game_name text NOT NULL,
    played_on date NOT NULL,
    user_id text,
    notes text,
    tags text[]
    );

-- migrate:down

DROP TABLE game_logs;
