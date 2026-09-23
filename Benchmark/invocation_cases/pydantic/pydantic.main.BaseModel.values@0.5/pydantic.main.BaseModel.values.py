from pydantic import BaseModel
import inspect

class User(BaseModel):
    id: int
    name: str

def main():
    user = User(id=1, name='John Doe')
    result = user.values()
    print("values result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseModel.values))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()