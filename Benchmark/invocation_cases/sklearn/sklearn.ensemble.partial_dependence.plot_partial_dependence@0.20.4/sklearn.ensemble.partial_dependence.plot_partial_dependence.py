import numpy as np
from sklearn.datasets import make_friedman1
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble.partial_dependence import plot_partial_dependence
import matplotlib.pyplot as plt
import inspect

def main():
    # Create sample data
    X, y = make_friedman1(n_samples=100, n_features=10, random_state=0)
    
    # Fit a model
    est = GradientBoostingRegressor(n_estimators=10, random_state=0)
    est.fit(X, y)
    
    # Plot partial dependence
    fig, ax = plt.subplots()
    plot_partial_dependence(est, X, [0, 1], ax=ax)
    plt.show()

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(plot_partial_dependence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()