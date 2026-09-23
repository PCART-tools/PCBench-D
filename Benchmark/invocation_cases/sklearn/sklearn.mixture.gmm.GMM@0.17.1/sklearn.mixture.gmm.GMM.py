import numpy as np
from sklearn.mixture import GMM
import inspect

def main():
    # Simulate some data
    np.random.seed(0)
    X = np.random.rand(100, 2)

    # Create and fit the GMM model
    gmm = GMM(n_components=2, covariance_type='full')
    gmm.fit(X)
    result = gmm.predict(X)
    print("GMM predict result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GMM))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()