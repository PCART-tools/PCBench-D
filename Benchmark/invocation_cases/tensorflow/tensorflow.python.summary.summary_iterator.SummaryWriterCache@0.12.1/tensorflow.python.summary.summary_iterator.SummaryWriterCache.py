from tensorflow.python.summary.summary_iterator import SummaryWriterCache,SummaryWriter
import inspect

def main():
    # Simulate using the SummaryWriterCache
    logdir = "/tmp/logs"
    writer = SummaryWriter(logdir)
    tool = SummaryWriterCache()
    cached_writer = tool.get(logdir)
    print("SummaryWriterCache result:", cached_writer is writer)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SummaryWriterCache))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
