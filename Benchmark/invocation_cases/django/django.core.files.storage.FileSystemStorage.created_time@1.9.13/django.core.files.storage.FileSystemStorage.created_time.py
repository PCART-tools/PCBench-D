import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import inspect

def main():
    # Configure Django settings
    settings.configure(
        DEBUG=True,
        MEDIA_ROOT=tempfile.gettempdir(),
        MEDIA_URL="/media/"
    )
    
    # Create a temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, 'test.txt')
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write('Hello, Django!')

    # Use FileSystemStorage to get the created time
    storage = FileSystemStorage(location=temp_dir)
    created_time = storage.created_time('test.txt')
    print("created_time result:", created_time)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FileSystemStorage.created_time))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()