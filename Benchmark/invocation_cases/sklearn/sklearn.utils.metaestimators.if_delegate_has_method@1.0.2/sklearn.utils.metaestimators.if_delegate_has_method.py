import inspect
from sklearn.utils.metaestimators import if_delegate_has_method

class DelegateWithFoo:
    def foo(self):
        return "foo from delegate"

class DelegateWithoutFoo:
    pass

class Estimator:
    def __init__(self, delegate):
        self.delegate = delegate

    @if_delegate_has_method(delegate="delegate")
    def foo(self):
        return self.delegate.foo()


def main():
    print("=== Case 1: delegate has foo method ===")
    est1 = Estimator(DelegateWithFoo())
    print(est1.foo()) 

    print("\n=== Case 2: delegate no foo method ===")
    est2 = Estimator(DelegateWithoutFoo())
    try:
        print(est2.foo()) 
    except AttributeError as e:
        print("Caught expected exception:", type(e).__name__)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(if_delegate_has_method))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
