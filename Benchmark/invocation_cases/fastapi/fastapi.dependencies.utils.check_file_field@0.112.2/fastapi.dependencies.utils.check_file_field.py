from fastapi import File, UploadFile
from fastapi.dependencies.utils import check_file_field
import inspect


class FakeModelField:
    def __init__(self):
        self.name = "file"
        self.type_ = UploadFile
        self.field_info = File(...)


def main():
    field = FakeModelField()
    check_file_field(field)
    print("check_file_field called successfully")
    

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(check_file_field))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()