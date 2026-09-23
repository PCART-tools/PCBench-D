import inspect
from django.db.backends.mysql.introspection import DatabaseIntrospection

class FakeOps:
    def quote_name(self, name):
        return "`%s`" % name

class FakeConnection:
    ops = FakeOps()

class FakeCursor:
    def execute(self, sql):
        print("SQL executed:", sql)

    def fetchall(self):
        return [
            # Table, Non_unique, Key_name, Seq_in_index, Column_name
            ('auth_user', 0, 'PRIMARY', 1, 'id'),
            ('auth_user', 1, 'username', 1, 'username'),
        ]

def main():
    connection = FakeConnection()
    introspection = DatabaseIntrospection(connection)

    cursor = FakeCursor()
    table_name = 'auth_user'
    result = introspection.get_indexes(cursor, table_name)

    print("get_indexes result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_indexes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
