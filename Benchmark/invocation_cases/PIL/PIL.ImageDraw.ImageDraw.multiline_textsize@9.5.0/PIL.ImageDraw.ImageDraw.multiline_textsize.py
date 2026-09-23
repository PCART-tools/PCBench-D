from PIL import Image, ImageDraw, ImageFont
import inspect

def main():
    # Create a blank image
    img = Image.new("RGB", (200, 200), color="white")
    draw = ImageDraw.Draw(img)
    
    # Define text and font
    text = "Hello\nWorld"
    font = ImageFont.load_default()
    
    # Call multiline_textsize
    size = draw.multiline_textsize(text, font=font)
    print("multiline_textsize result:", size)
    
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ImageDraw.ImageDraw.multiline_textsize))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()