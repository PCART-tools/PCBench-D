from faker import Faker
from faker.providers import BaseProvider
import inspect

def main():
    fake = Faker()
    result = BaseProvider.random_sample_unique(fake,elements=('a', 'b', 'c', 'd', 'e'), length=3)
    print("random_sample_unique result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseProvider.random_sample_unique))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()