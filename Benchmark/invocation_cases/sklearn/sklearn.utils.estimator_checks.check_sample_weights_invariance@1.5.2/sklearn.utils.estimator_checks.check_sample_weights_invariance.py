import inspect
from sklearn.linear_model import LinearRegression
from sklearn.utils.estimator_checks import check_sample_weights_invariance


def main():
    estimator = LinearRegression()
    check_sample_weights_invariance(
        name="LinearRegression",
        estimator_orig=estimator,
        kind="ones",
    )
    print("check_sample_weights_invariance(kind='ones'): PASS")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(check_sample_weights_invariance))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()