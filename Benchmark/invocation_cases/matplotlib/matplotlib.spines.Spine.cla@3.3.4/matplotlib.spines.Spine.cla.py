import matplotlib.pyplot as plt
import inspect

def main():
    fig, ax = plt.subplots()
    spine = ax.spines['left']
    spine.cla()
    print("Spine cla called successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(spine.cla))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()