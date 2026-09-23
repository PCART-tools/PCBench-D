import matplotlib.textpath as mtextpath
from matplotlib.font_manager import FontProperties
import inspect

def main():
    prop = FontProperties()
    text_path = mtextpath.TextPath((0, 0), "Hello", prop=prop)
    vertices, codes = text_path.text_get_vertices_codes(
        s="Hello",
        prop=prop,
        usetex=False
    )
    print("Vertices:", vertices)
    print("Codes:", codes)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(text_path.text_get_vertices_codes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()