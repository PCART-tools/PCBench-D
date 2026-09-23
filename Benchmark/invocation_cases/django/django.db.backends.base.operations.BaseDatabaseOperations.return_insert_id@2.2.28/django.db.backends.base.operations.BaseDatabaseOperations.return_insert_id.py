import inspect
from django.db.backends.base.operations import BaseDatabaseOperations

def main():
    class MockDatabaseOperations(BaseDatabaseOperations):
        pass

    mock_ops = MockDatabaseOperations(None)
    result = mock_ops.return_insert_id()
    print("return_insert_id result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mock_ops.return_insert_id))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()