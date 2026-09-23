import tensorflow as tf
import inspect

class MyTest(tf.test.TestCase):
    def test_example(self):
        with self.test_session() as sess:
            print("reached test_session")

def main():
    test_case = MyTest()
    test_case.test_example()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(tf.test.TestCase.test_session))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()