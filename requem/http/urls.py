def database_url(database):
    return '/database/%s/' % database


def database_connection_url(database, connection_id):
    return '/database/%s/conn/%d' % (database, connection_id)


def database_cursor_url(database, connection_id, cursor_id):
    return '/database/%s/conn/%d/cursor/%d' % (database, connection_id, cursor_id)