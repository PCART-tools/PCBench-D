import matplotlib.pyplot as plt
import inspect
import datetime

def main():
    dates = [datetime.date(2023, 12, i) for i in range(1, 6)]
    values = [1, 2, 3, 4, 5]
    result = plt.plot_date(dates, values)
    print("plot_date result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(plt.plot_date))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()