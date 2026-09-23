import django
from django.db.backends.mysql.introspection import DatabaseIntrospection
import inspect

# ===== mock connection.ops =====
class FakeOps:
    def quote_name(self, name):
        return f"`{name}`"


class FakeConnection:
    ops = FakeOps()


# ===== mock cursor =====
class FakeCursor:
    def execute(self, sql, params=None):
        print("SQL executed:", sql)
        print("params:", params)

    def fetchall(self):
        return [
            ('user_id', 'id'),
            ('group_id', 'id'),
        ]


def main():
    connection = FakeConnection()
    introspection = DatabaseIntrospection(connection)

    cursor = FakeCursor()
    key_columns = introspection.get_key_columns(cursor, 'test_table')


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_key_columns))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()