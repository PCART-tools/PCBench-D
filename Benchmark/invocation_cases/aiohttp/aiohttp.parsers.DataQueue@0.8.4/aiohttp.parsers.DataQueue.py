import aiohttp.parsers
import inspect

def main():
    stream = aiohttp.parsers.StreamParser()
    queue = aiohttp.parsers.DataQueue(stream)
    result = queue.at_eof()
    print("DataQueue at_eof result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(aiohttp.parsers.DataQueue))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()