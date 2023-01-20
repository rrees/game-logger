-- migrate:up

ALTER TABLE game_logs
ADD COLUMN system text;
