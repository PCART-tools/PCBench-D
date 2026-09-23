@register_meta(aten.addcdiv)
@out_wrapper()
def addcdiv(input, tensor1, tensor2, *, value=1):
    torch._check(
        not (
            utils.is_integer_dtype(tensor1.dtype)
            and utils.is_integer_dtype(tensor2.dtype)
        ),
        lambda: (
            "Integer division with addcdiv is no longer supported, and in a future ",
            "release addcdiv will perform a true division of tensor1 and tensor2. ",
            "The historic addcdiv behavior can be implemented as ",
            "(input + value * torch.trunc(tensor1 / tensor2)).to(input.dtype) ",
            "for integer inputs and as ",
            "(input + value * tensor1 / tensor2) for float inputs. ",
            "The future addcdiv behavior is just the latter implementation: ",
            "(input + value * tensor1 / tensor2), for all dtypes.",
        ),
    )
    return elementwise_meta(
        input, tensor1, tensor2, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
