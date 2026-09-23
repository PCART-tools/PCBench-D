import inspect
import os
from pydantic.types import FilePath

def main():
    file_name = "temp_file.txt"
    with open(file_name, "w") as f:
        f.write("test")

    validators = list(FilePath.get_validators())
    validator = validators[0]

    result = validator(file_name)
    print("Validation success:", result)
    os.remove("temp_file.txt")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FilePath.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()