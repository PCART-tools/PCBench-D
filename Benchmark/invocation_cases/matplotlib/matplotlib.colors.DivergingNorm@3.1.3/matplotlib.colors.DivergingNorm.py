import matplotlib.colors as mcolors
import inspect
import numpy as np

def main():
    data = np.array([-1, 0, 1, 2, 3])
    norm = mcolors.DivergingNorm(vmin=-1, vcenter=1, vmax=3)
    normalized_data = norm(data)
    print("DivergingNorm result:", normalized_data)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mcolors.DivergingNorm))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()