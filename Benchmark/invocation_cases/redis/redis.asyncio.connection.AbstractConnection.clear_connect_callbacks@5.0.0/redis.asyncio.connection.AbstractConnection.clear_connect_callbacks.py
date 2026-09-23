import asyncio
import inspect
from redis.asyncio.connection import AbstractConnection

class TestConnection(AbstractConnection):
    async def _connect(self):
        self._connected = True

    async def _disconnect(self):
        self._connected = False


async def main():
    connection = TestConnection()
    async def cb1(conn): pass
    async def cb2(conn): pass
    connection._connect_callbacks.append(cb1)
    connection._connect_callbacks.append(cb2)

    print("before clear:", len(connection._connect_callbacks))
    result = connection.clear_connect_callbacks()

    print("clear_connect_callbacks result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(TestConnection.clear_connect_callbacks))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    asyncio.run(main())