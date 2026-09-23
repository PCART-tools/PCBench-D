import matplotlib
matplotlib.use('Agg') 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
import inspect


def main():
    dates = [datetime.datetime(2020, 1, i + 1) for i in range(10)]
    values = range(10)

    x = list(range(len(dates)))

    fig, ax = plt.subplots()
    ax.plot(x, values)

    formatter = mdates.IndexDateFormatter(dates, fmt='%Y-%m-%d')

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mdates.IndexDateFormatter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()