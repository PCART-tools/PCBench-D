import pandas as pd
import numpy as np
import inspect

def main():
    # Create a DataFrame with random data
    df = pd.DataFrame(np.random.rand(10, 4), columns=['A', 'B', 'C', 'D'])
    
    # Call the scatter_matrix function
    pd.tools.plotting.scatter_matrix(df)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pd.tools.plotting.scatter_matrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()