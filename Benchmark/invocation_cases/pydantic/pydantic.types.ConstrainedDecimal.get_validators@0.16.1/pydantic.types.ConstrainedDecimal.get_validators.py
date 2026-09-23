from pydantic.types import ConstrainedDecimal
from decimal import Decimal
import inspect

def main():
    class MyDecimal(ConstrainedDecimal):
        gt = 0
        lt = 100
        
    validators = list(MyDecimal.get_validators())
    print("get_validators result:", validators)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MyDecimal.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()