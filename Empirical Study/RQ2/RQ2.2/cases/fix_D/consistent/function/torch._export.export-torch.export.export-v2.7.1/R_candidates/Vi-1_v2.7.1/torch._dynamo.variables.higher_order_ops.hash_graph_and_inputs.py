def hash_graph_and_inputs(tx, gmod, fake_inputs):
    # Here, we use the existing autograd_cache_key infrastructure to hash the
    # graph and fake inputs.

    # TODO(anijain2305) - Consider reorganizing autograd_cache_key such that the
    # namespaces seem more intuitive. It seems somewhat confusing that we are
    # calling an API from aot_autograd here.
    from torch._functorch._aot_autograd.autograd_cache import autograd_cache_key

    # autograd_cache_key is sensitive to the name of the placeholder nodes.
    # So, we first canonicalize it.
    canonicalized_gmod = canonicalize(gmod, tx.output.nn_modules)
    config = get_dummy_aot_autograd_config()

    key, _ = autograd_cache_key(canonicalized_gmod, fake_inputs, config, {})
    return key
