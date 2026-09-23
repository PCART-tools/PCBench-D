from pydantic import EmailStr
import inspect

def main():
    email = EmailStr('test@example.com')
    validators = list(email.get_validators())
    print("get_validators result:", validators)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(EmailStr.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()