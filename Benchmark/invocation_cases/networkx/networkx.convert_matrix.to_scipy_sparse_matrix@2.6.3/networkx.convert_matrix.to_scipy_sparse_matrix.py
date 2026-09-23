import networkx as nx
import inspect
from scipy.sparse import csr_matrix

def main():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4)])
    result = nx.to_scipy_sparse_matrix(G)
    print("to_scipy_sparse_matrix result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(nx.to_scipy_sparse_matrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()