import redis
from redis.connection import AbstractConnection
import inspect

class TestAbstractConnection(AbstractConnection):
    def _connect(self):
        pass

    def disconnect(self):
        pass


def main():
    connection = TestAbstractConnection()

    AbstractConnection.clear_connect_callbacks(connection)
    print("AbstractConnection.clear_connect_callbacks called successfully")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(AbstractConnection.clear_connect_callbacks))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()