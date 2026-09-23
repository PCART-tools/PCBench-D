import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import inspect

def main():
    # Sample data
    X = np.array([
        ['Male', 1],
        ['Female', 3],
        ['Female', 2]
    ], dtype=object)

    # Define ColumnTransformer (exclude StandardScaler which lacks get_feature_names in 0.24.2)
    column_transformer = ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(), [0])
        ]
    )

    # Fit the data
    column_transformer.fit(X)

    # Get feature names (scikit-learn 0.24.2 API)
    feature_names = column_transformer.get_feature_names()
    print("Feature names:", feature_names)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ColumnTransformer.get_feature_names))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
