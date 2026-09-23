import inspect
from django.db.backends.oracle.introspection import DatabaseIntrospection

# ===== mock connection.ops =====
class FakeOps:
    def quote_name(self, name):
        return f'"{name.upper()}"'


class FakeConnection:
    ops = FakeOps()


# ===== mock cursor =====
class FakeCursor:
    def execute(self, sql, params=None):
        print("SQL executed:", sql)
        print("params:", params)

    def fetchall(self):
        # (index_name, uniqueness, column_name)
        return [
            ('SYS_C001234', 'UNIQUE', 'ID'),
            ('IDX_MY_TABLE_NAME', 'NONUNIQUE', 'NAME'),
        ]


def main():
    connection = FakeConnection()
    introspection = DatabaseIntrospection(connection)

    cursor = FakeCursor()
    table_name = 'my_table'

    result = introspection.get_key_columns(cursor, table_name)
    print("get_key_columns result:", result)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_key_columns))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()