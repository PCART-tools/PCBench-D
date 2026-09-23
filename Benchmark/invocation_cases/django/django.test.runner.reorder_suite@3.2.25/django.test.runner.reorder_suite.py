import django
from django.test.runner import reorder_suite
import unittest
import inspect

def main():
    # Create a simple test suite
    class TestExample(unittest.TestCase):
        def test_one(self):
            pass

        def test_two(self):
            pass

    suite = unittest.TestSuite()
    suite.addTest(TestExample('test_one'))
    suite.addTest(TestExample('test_two'))

    # Call reorder_suite
    reordered_suite = reorder_suite(suite, (TestExample,))
    print("Reordered suite:", reordered_suite)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(reorder_suite))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()