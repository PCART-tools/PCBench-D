def _make_grads(outputs: Sequence[torch.Tensor], grads: Sequence[_OptionalTensor]) -> Tuple[_OptionalTensor, ...]:
    new_grads: List[_OptionalTensor] = []
    for out, grad in zip(outputs, grads):
        if isinstance(grad, torch.Tensor):
            if not out.shape == grad.shape:
                raise RuntimeError("Mismatch in shape: grad_output["
                                   + str(grads.index(grad)) + "] has a shape of "
                                   + str(grad.shape) + " and output["
                                   + str(outputs.index(out)) + "] has a shape of "
                                   + str(out.shape) + ".")
            if out.dtype.is_complex != grad.dtype.is_complex:
                raise RuntimeError("For complex Tensors, both grad_output and output"
                                   " are required to have the same dtype."
                                   " Mismatch in dtype: grad_output["
                                   + str(grads.index(grad)) + "] has a dtype of "
                                   + str(grad.dtype) + " and output["
                                   + str(outputs.index(out)) + "] has a dtype of "
                                   + str(out.dtype) + ".")
            new_grads.append(grad)
        elif grad is None:
            if out.requires_grad:
                if out.numel() != 1:
                    raise RuntimeError("grad can be implicitly created only for scalar outputs")
                new_grads.append(torch.ones_like(out, memory_format=torch.preserve_format))
            else:
                new_grads.append(None)
        else:
            raise TypeError("gradients can be either Tensors or None, but got " +
                            type(grad).__name__)
    return tuple(new_grads)
