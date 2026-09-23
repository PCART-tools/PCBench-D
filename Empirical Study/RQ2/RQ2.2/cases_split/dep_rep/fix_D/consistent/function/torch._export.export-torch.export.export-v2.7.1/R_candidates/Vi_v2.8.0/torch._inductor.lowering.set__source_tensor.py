@register_lowering(torch.ops.aten.set_.source_Tensor)
def set__source_tensor(self, source_tensor):
    self.realize()
    source_tensor.realize()
    return TensorBox.create(ir.SetSourceTensorKernel(self, source_tensor))
