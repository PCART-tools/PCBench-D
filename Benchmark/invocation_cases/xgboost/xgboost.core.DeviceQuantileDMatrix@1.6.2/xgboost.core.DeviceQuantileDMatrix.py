import xgboost as xgb
import cupy as cp
import numpy as np
import inspect

def main():
    # Simulate input data with CuPy
    data = cp.random.rand(100, 10).astype(cp.float32)
    label = cp.random.randint(0, 2, size=100).astype(cp.float32)

    # Create DeviceQuantileDMatrix using GPU data
    dmatrix = xgb.DeviceQuantileDMatrix(
        data=data,
        label=label,
        max_bin=256
    )
    print("DeviceQuantileDMatrix created:", dmatrix)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(xgb.DeviceQuantileDMatrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
