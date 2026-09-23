def addcmul_inplace(self, tensor1, tensor2, value):
    return self.add_(tensor1 * tensor2 * value)
