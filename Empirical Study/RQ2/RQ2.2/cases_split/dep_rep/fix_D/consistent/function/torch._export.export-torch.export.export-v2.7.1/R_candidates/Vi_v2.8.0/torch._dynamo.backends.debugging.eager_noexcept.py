@register_backend
def eager_noexcept(gm, fake_tensor_inputs, **kwargs):
    if kwargs:
        log.warning("eager_noexcept backend ignoring extra kwargs %s", kwargs)

    # This backend is intended to check that dynamo-generated GraphModules
    # do not cause errors.
    def inner(*args):
        try:
            return gm(*args)
        except Exception as e:
            raise torch._dynamo.exc.TorchDynamoException(
                "Unexpected exception when running generated GraphModule"
            ) from e

    return inner
