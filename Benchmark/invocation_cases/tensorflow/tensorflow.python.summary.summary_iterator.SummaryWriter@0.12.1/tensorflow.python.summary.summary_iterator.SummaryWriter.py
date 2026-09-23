from tensorflow.python.summary.summary_iterator import SummaryWriter
import inspect

def main():
    logdir = "/tmp/logs"
    writer = SummaryWriter(logdir)
    print("SummaryWriter created with logdir:", logdir)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SummaryWriter))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()