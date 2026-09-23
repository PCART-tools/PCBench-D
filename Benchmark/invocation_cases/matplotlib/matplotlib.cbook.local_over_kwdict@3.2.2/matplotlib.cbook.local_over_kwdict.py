import matplotlib.cbook as cbook
import inspect

def main():
    defaults = {'color': 'blue', 'linewidth': 2}
    kwargs = {'linewidth': 3}
    result = cbook.local_over_kwdict(defaults, kwargs)
    print("local_over_kwdict result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbook.local_over_kwdict))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()