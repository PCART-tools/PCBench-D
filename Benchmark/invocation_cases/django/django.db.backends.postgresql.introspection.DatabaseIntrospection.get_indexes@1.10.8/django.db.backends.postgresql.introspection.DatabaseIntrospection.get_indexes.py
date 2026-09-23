import django
from django.db.backends.postgresql.introspection import DatabaseIntrospection
import inspect

# ===== mock connection.ops =====
class FakeOps:
    def quote_name(self, name):
        return f'"{name}"'


class FakeConnection:
    ops = FakeOps()


# ===== mock cursor =====
class FakeCursor:
    def execute(self, sql, params=None):
        print("SQL executed:", sql)
        print("params:", params)

    def fetchall(self):
        # (column_name, index_name, unique, primary_key)
        return [
            ('id', 'my_table_pkey', True, True),
            ('username', 'my_table_username_key', True, False),
            ('email', 'my_table_email_idx', False, False),
        ]

def main():
    connection = FakeConnection()
    introspection = DatabaseIntrospection(connection)

    cursor = FakeCursor()
    table_name = 'my_table'

    indexes = introspection.get_indexes(cursor, table_name)
    print("get_indexes result:", indexes)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_indexes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()