import inspect
from django.db.backends.base.operations import BaseDatabaseOperations

def main():
    # Create a mock BaseDatabaseOperations instance
    class MockDatabaseOperations(BaseDatabaseOperations):
        pass
    
    class FakeCursor:
        def fetchone(self):
            return (123,)
        
    mock_operations = MockDatabaseOperations(connection=None)
    cursor = FakeCursor()

    # Call the target API
    result = mock_operations.fetch_returned_insert_id(cursor)
    print("fetch_returned_insert_id result:", result)

    # Get the source code of the target API
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseDatabaseOperations.fetch_returned_insert_id))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()