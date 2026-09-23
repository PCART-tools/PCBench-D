import sys
import polars as pl
import pyarrow as pa
import inspect


def _install_fake_connectorx():
    def fake_read_sql(**kwargs):
        return pa.table({"a": [1, 2, 3]})

    class FakeConnectorX:
        read_sql = staticmethod(fake_read_sql)

    sys.modules["connectorx"] = FakeConnectorX


def test_read_sql_basic():
    _install_fake_connectorx()

    df = pl.read_sql(
        "SELECT 1",
        connection_uri="postgresql://user:pwd@localhost:5432/db",
    )

def main():

    test_read_sql_basic()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pl.read_sql))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
