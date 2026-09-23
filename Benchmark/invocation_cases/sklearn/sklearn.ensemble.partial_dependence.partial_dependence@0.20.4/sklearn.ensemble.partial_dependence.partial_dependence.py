import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble.partial_dependence import partial_dependence
import inspect

def main():
    # Create a simple classification dataset
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    
    # Train a GradientBoostingClassifier (compatible with partial_dependence in v0.20.4)
    clf = GradientBoostingClassifier(n_estimators=10, random_state=42)
    clf.fit(X, y)

    # Compute partial dependence for the first feature
    result = partial_dependence(clf, [0], X=X)
    print("partial_dependence result:", result)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(partial_dependence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
