from PIL import ImageFont
import inspect
import os

def find_font(preferred_fonts=None):
    if preferred_fonts is None:
        preferred_fonts = ["arial.ttf", "DejaVuSans.ttf"]
    
    for font_name in preferred_fonts:
        try:
            font = ImageFont.truetype(font_name, size=20)
            return font
        except OSError:
            continue
    raise RuntimeError("No usable TrueType font found.")

def main():
    font = find_font()
    
    # Call the getsize method
    text = "Hello, Pillow!"
    size = font.getsize(text)
    print("getsize result:", size)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ImageFont.FreeTypeFont.getsize))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()