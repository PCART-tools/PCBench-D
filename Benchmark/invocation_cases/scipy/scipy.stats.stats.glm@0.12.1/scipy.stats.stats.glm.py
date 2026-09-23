import numpy as np
import inspect
from scipy.stats import glm

def main():
    data = np.array([1.1, 1.3, 1.2, 2.0, 2.2, 2.1])
    para = np.array([0, 0, 0, 1, 1, 1]) 

    t_stat, p_value = glm(data, para)

    print("t statistic:", t_stat)
    print("p value:", p_value)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(glm))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()