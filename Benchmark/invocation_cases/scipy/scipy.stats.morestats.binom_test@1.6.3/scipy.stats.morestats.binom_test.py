import scipy.stats as stats
import inspect

def main():
    result = stats.binom_test(5, n=10, p=0.5)
    print("binom_test result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(stats.binom_test))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()