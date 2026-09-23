def main():
    run(n=100, stmt="torch.sparse.sum(x, dim=0)", fuzzer_cls=UnaryOpSparseFuzzer)
    run(n=100, stmt="torch.sparse.softmax(x, dim=0)", fuzzer_cls=UnaryOpSparseFuzzer)
    run(n=100, stmt="x + y", fuzzer_cls=BinaryOpSparseFuzzer)
