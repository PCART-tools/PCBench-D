import numpy as np
from scipy.signal import impulse2, lti
import inspect

def main():
    # Define a simple LTI system
    system = lti([1.0], [1.0, 1.0])
    
    # Compute the impulse response
    t, y = impulse2(system)
    print("Impulse response (t):", t)
    print("Impulse response (y):", y)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(impulse2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()