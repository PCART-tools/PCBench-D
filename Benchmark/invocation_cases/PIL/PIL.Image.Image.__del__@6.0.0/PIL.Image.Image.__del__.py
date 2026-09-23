from PIL import Image
import inspect

def main():
    img = Image.new('RGB', (100, 100), color='red')

    Image.Image.__del__(img)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Image.Image.__del__))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()