from PIL import ImageFile
import inspect

def main():
    try:
        # Invoke the raise_ioerror function directly as defined in PIL.ImageFile
        ImageFile.raise_ioerror(1)
    except OSError as e:
        print("raise_ioerror result:", str(e))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ImageFile.raise_ioerror))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
