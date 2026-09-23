@register_meta(aten.addcmul)
@out_wrapper()
def addcmul(input, tensor1, tensor2, *, value=1):
    return elementwise_meta(
        input, tensor1, tensor2, type_promotion=ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT
    )
