import numpy as np
import inspect

def main():
    formats = ['i4', 'f4', 'a10']
    names = ['field1', 'field2', 'field3']
    titles = ['title1', 'title2', 'title3']
    
    parser = np.core.records.format_parser(formats, names, titles)
    result = parser.dtype.descr
    print("format_parser result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(np.core.records.format_parser))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()