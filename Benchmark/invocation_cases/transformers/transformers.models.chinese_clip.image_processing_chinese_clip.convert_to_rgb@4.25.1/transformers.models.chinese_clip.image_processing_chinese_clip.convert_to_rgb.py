import inspect
from transformers.models.chinese_clip.image_processing_chinese_clip import convert_to_rgb
from PIL import Image
import numpy as np

def main():
    # Create a dummy image with random data
    image_data = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    image = Image.fromarray(image_data)

    # Call the convert_to_rgb function
    result = convert_to_rgb(image)
    print("convert_to_rgb result:", result.mode)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(convert_to_rgb))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()