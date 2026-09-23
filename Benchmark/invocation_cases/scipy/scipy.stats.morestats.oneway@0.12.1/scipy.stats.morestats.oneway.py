import scipy.stats.morestats as morestats
import inspect

def main():
    # Simulated input data for the oneway function
    group1 = [1.2, 2.3, 3.1]
    group2 = [2.1, 3.4, 1.8]
    group3 = [1.5, 2.7, 3.0]
    
    result = morestats.oneway(group1, group2, group3)
    print("oneway result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(morestats.oneway))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()