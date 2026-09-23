from PIL import ImageMath
import inspect

def main():
    expression = "a + b"
    variables = {"a": 5, "b": 3}
    result = ImageMath.eval(expression, **variables)
    print("ImageMath.eval result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ImageMath.eval))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()