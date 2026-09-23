@register_experimental_backend
def openxla_eval(model, fake_tensor_inputs):
    return xla_backend_helper(model, fake_tensor_inputs, boxed=False)
