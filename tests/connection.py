from quelo import get_value, get_column
from quelo.error import UniqueColumnsConstraintViolation, PrimaryKeyViolation, TableNotExisting, ForeignKeyError


def test_connection(cursor):
    cursor.execute('''delete from full_name''')

    cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('hulk', 'hogan'))
    cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('mr', 't'))

    assert get_value(cursor, 'select name from full_name where surname = ?', ('hogan', )) == 'hulk'

    assert cursor.select('select name, surname from full_name') == [('hulk', 'hogan'), ('mr', 't')]
    assert get_column(cursor, '''select name from full_name''') == ['hulk', 'mr']

    try:
        cursor.execute('''insert into full_name(name, surname)
                                    values(?,?) ''', ('hulk', 'hogan'))

    except UniqueColumnsConstraintViolation, e:
        print e
        assert e.columns == ['name', 'surname']

    full_name_id = get_value(cursor, '''select id
                                                  from full_name
                                                 where name = ?
                                                   and surname = ? ''', ('hulk', 'hogan'))

    try:
        cursor.execute('''insert into full_name(id, name, surname)
                                    values(?,?,?) ''', (full_name_id, 'corky', 'butchek'))
    except PrimaryKeyViolation, e:
        print e

    try:
        cursor.execute('''insert into unknown(id) values(1)''')
    except TableNotExisting, e:
        print e

    try:
        cursor.execute('''insert into person(full_name_id, social_number)
                                    values(?,?)''', (-1, 'the_hulk'))
    except ForeignKeyError, e:
        print e
