import numpy as np
from scipy.signal import lti, lsim2
import inspect

def main():
    # Define a simple LTI system
    system = lti([1.0], [1.0, 1.0])  # Transfer function: H(s) = 1 / (s + 1)
    t = np.linspace(0, 10, 100)  # Time vector
    u = np.sin(t)  # Input signal (sine wave)

    # Simulate the system response
    t_out, y_out, x_out = lsim2(system, U=u, T=t)
    print("lsim2 output (t_out, y_out, x_out):")
    print("t_out:", t_out)
    print("y_out:", y_out)
    print("x_out:", x_out)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(lsim2))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()