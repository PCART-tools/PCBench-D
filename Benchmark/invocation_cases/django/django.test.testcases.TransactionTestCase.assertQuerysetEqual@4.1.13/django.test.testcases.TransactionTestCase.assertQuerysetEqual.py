import inspect
import django
from django.conf import settings
from django.test.testcases import TransactionTestCase


settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        '__main__',
    ],
)

django.setup()

class MyTestCase(TransactionTestCase):
    def test_assertQuerysetEqual(self):
        data = ["Item1", "Item2"]
        expected = ["Item1", "Item2"]
        self.assertQuerysetEqual(data, expected)

def main():
    test_case = MyTestCase()
    test_case.test_assertQuerysetEqual()
    print("assertQuerysetEqual passed")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(TransactionTestCase.assertQuerysetEqual))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()