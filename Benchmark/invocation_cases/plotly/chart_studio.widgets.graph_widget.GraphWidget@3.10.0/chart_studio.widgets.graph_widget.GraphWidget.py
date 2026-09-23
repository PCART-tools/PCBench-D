import plotly
import inspect
from chart_studio.widgets import GraphWidget

def main():
    # Simulate test data
    graph_url = "https://plot.ly/~username/0"
    
    # Create a GraphWidget instance
    widget = GraphWidget(graph_url)
    print("GraphWidget instance created:", widget)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GraphWidget))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()