import matplotlib.backends.backend_pdf as mbbp
import matplotlib.pyplot as plt
import numpy as np
import inspect
from matplotlib import transforms

def main():
    # Create a PDF file to draw on
    pdf = mbbp.PdfPages('output.pdf') 
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    pdf.savefig(fig)

    # Get figure size and dpi
    dpi = fig.dpi
    width, height = fig.get_size_inches()

    # Create RendererPdf object
    renderer = mbbp.RendererPdf(pdf._file, dpi, height, width)

    # Create a graphics context
    gc = renderer.new_gc()

    # Define triangle vertices: shape (3, 2)
    points = np.array([[0.2, 0.2],
                       [0.8, 0.2],
                       [0.5, 0.8]], dtype=np.float32)

    # Define RGBA colors: shape (3, 4)
    colors = np.array([[1, 0, 0, 1],   # Red
                       [0, 1, 0, 1],   # Green
                       [0, 0, 1, 1]],  # Blue
                      dtype=np.float32)

    # Affine transformation to map data to PDF space
    trans = transforms.Affine2D().scale(72)  # 1 inch = 72 points

    # Correct call with all required arguments
    renderer.draw_gouraud_triangle(gc, points, colors, trans)
    print("draw_gouraud_triangle called successfully")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbbp.RendererPdf.draw_gouraud_triangle))
    except Exception as e:
        print(type(e).__name__)

    # Cleanup
    gc.restore()
    pdf.close()

if __name__ == "__main__":
    main()
