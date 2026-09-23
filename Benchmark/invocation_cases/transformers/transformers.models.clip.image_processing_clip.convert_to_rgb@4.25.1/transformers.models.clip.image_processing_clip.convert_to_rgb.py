import inspect
from transformers.models.clip.image_processing_clip import convert_to_rgb
from PIL import Image
import numpy as np

def main():
    # Create a dummy grayscale image
    grayscale_image = Image.fromarray(np.random.randint(0, 255, (100, 100), dtype=np.uint8))

    # Convert the grayscale image to RGB
    rgb_image = convert_to_rgb(grayscale_image)
    print("Converted image mode:", rgb_image.mode)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(convert_to_rgb))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()