import numpy as np
from scipy.signal import step2, TransferFunction
import inspect

def main():
    # Define a simple transfer function H(s) = 1 / (s + 1)
    num = [1]
    den = [1, 1]
    system = TransferFunction(num, den)
    
    # Compute the step response
    t, y = step2(system)
    print("Step response time values:", t)
    print("Step response output values:", y)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(step2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()