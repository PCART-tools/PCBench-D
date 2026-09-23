import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import is_aware, make_naive
import inspect
from django.conf import settings

def main():
    # Configure settings
    settings.configure()

    # Create a temporary file to test accessed_time
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, "test_file.txt")
    with open(file_path, "w") as f:
        f.write("Test content")

    # Initialize FileSystemStorage
    storage = FileSystemStorage(location=temp_dir)

    # Call accessed_time
    accessed_time = storage.accessed_time("test_file.txt")
    if is_aware(accessed_time):
        accessed_time = make_naive(accessed_time)
    print("accessed_time result:", accessed_time)

    # Get source code of accessed_time
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(storage.accessed_time))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()