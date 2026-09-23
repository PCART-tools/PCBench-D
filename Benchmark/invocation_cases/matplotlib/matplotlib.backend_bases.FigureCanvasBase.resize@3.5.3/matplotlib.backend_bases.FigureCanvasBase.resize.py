import matplotlib.backend_bases as mbb
import inspect

def main():
    # Create a mock subclass of FigureCanvasBase to test the resize method
    class MockCanvas(mbb.FigureCanvasBase):
        def __init__(self):
            super().__init__(None)
        
    canvas = MockCanvas()
    canvas.resize(800, 600)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mbb.FigureCanvasBase.resize))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()