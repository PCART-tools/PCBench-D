import numpy as np
from scipy.signal._filter_design import sosfreqz
import inspect

def main():
    sos = np.array([
        [1.0, 0.0, 0.0,   1.0, 0.0, 0.0]
    ])

    w, h = sosfreqz(sos)
    print("frequency points w:")
    print(w[:5], "...")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sosfreqz))
    except Exception as e:
        print(type(e).__name__)

if __name__=="__main__":
    main()