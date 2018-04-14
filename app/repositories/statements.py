
delete_user_log = '''
DELETE FROM game_logs
WHERE log_id = %(log_id)s
AND user_id = %(user_id)s
'''

delete_log = '''
DELETE FROM game_logs
WHERE log_id = %(log_id)s
'''