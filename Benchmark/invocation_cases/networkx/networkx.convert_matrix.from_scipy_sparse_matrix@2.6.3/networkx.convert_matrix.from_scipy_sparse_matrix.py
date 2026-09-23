import networkx as nx
from scipy.sparse import csr_matrix
import inspect

def main():
    # Create a scipy sparse matrix
    sparse_matrix = csr_matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    
    # Convert the sparse matrix to a NetworkX graph
    graph = nx.from_scipy_sparse_matrix(sparse_matrix)
    print("Graph nodes:", graph.nodes())
    print("Graph edges:", graph.edges())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.from_scipy_sparse_matrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()