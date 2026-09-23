def addmm(self: list[int], mat1: list[int], mat2: list[int], beta: Any, alpha: Any):
    return broadcast(self, mm(mat1, mat2))
