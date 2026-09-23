import matplotlib.cbook as cbook
import inspect

def main():
    sequence = [1, 2, 3, None, "text"]
    result = cbook.sanitize_sequence(sequence)
    print("sanitize_sequence result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(cbook.sanitize_sequence))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()