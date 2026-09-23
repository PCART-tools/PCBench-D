def read_matrix_params(path):
    with open(path, 'r') as file:
        line = file.readline()
        nrows, ncols, nnz = map(lambda el: int(el), line.split(', '))
        return (nrows, ncols), nnz
