import torch
import inspect
from torch.ao.quantization.fx.quantization_patterns import EmbeddingQuantizeHandler
from torch.fx.node import Node
from torch.fx.graph import Graph

def create_dummy_node():
    graph = Graph()
    placeholder = graph.placeholder("x")
    embedding_node = graph.call_module("embedding", args=(placeholder,))
    return embedding_node

def main():
    # Create dummy node and module dict
    dummy_node = create_dummy_node()
    dummy_modules = {"embedding": torch.nn.Embedding(10, 3)}

    # Create EmbeddingQuantizeHandler instance
    handler = EmbeddingQuantizeHandler(dummy_node, dummy_modules)
    print("EmbeddingQuantizeHandler instance:", handler)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(EmbeddingQuantizeHandler))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
