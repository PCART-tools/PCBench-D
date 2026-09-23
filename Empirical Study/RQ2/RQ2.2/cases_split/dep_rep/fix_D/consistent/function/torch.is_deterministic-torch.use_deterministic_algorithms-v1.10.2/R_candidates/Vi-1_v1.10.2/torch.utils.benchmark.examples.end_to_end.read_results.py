def read_results(result_file: str):
    output = []
    with open(result_file, "rb") as f:
        while True:
            try:
                output.append(pickle.load(f))
            except EOFError:
                break
    return output
