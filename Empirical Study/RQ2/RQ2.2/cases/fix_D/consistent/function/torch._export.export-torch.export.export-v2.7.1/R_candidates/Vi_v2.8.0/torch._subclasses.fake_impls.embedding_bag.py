@register_op_impl(aten._embedding_bag.default)
def embedding_bag(fake_mode, func, *args, **kwargs):
    from torch._meta_registrations import meta_embedding_bag

    with fake_mode:
        return meta_embedding_bag(*args, **kwargs)
