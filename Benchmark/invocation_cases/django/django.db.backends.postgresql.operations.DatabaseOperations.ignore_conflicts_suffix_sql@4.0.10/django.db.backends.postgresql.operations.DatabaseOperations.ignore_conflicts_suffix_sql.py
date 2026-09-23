import django
from django.db.backends.postgresql.operations import DatabaseOperations
import inspect

def main():
    db_ops = DatabaseOperations(connection=None)
    result = db_ops.ignore_conflicts_suffix_sql()
    print("ignore_conflicts_suffix_sql result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseOperations.ignore_conflicts_suffix_sql))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()