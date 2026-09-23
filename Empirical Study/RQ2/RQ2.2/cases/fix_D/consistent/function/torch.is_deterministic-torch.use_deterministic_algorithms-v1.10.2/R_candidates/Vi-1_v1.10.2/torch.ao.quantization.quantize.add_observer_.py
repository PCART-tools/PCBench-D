def add_observer_(module, qconfig_propagation_list=None, non_leaf_module_list=None, device=None, custom_module_class_mapping=None):
    r"""Add observer for the leaf child of the module.

    This function insert observer module to all leaf child module that
    has a valid qconfig attribute.

    Args:
        module: input module with qconfig attributes for all the leaf modules that we want to quantize
        device: parent device, if any
        non_leaf_module_list: list of non-leaf modules we want to add observer

    Return:
        None, module is modified inplace with added observer modules and forward_hooks
    """
    if qconfig_propagation_list is None:
        qconfig_propagation_list = get_default_qconfig_propagation_list()

    if custom_module_class_mapping is None:
        custom_module_class_mapping = {}

    # respect device affinity when adding observers
    if device is None:
        devices = get_unique_devices_(module)
        assert len(devices) <= 1, (
            "add_observer_ only works with cpu or single-device CUDA modules, "
            "but got devices {}".format(devices)
        )
        device = next(iter(devices)) if len(devices) > 0 else None

    def get_activation_post_process(qconfig, device, special_act_post_process=None):
        activation = qconfig.activation() if special_act_post_process is None else special_act_post_process()
        if device is not None:
            activation.to(device)
        return activation

    def needs_observation(m):
        return hasattr(m, 'qconfig') and m.qconfig is not None

    def insert_activation_post_process(m, special_act_post_process=None):
        """ Adds an activation post process module and register
        a post hook that calls the module
        """
        # We don't insert observer/fake_quantize for DeQuantStub
        if needs_observation(m) and not isinstance(m, DeQuantStub):
            # observer and hook will be gone after we swap the module
            m.add_module('activation_post_process', get_activation_post_process(
                m.qconfig, device, special_act_post_process))
            # Register observer as the first entry in the hook list
            # All post forward hooks are preserved and will be executed after the observer before convert
            handle = register_activation_post_process_hook(m)
            m._forward_hooks.move_to_end(handle.id, last=False)

    for name, child in module.named_children():
        if type(child) in [nnq.FloatFunctional, nnq.QFunctional]:
            if needs_observation(child):
                child.activation_post_process = get_activation_post_process(child.qconfig, device)
        elif isinstance(child, _FusedModule):
            # activation_post_process are now added directly to nn.Sequentail/_FusedModule
            if needs_observation(child):
                insert_activation_post_process(child)
        elif _has_special_act_post_process(child):
            special_act_post_process = _get_special_act_post_process(child)
            insert_activation_post_process(child, special_act_post_process)
        elif non_leaf_module_list is not None and type(child) in non_leaf_module_list:
            if needs_observation(child):
                insert_activation_post_process(child)
        elif needs_observation(child) and type(child) in custom_module_class_mapping:
            observed_child = custom_module_class_mapping[type(child)].from_float(child)
            setattr(module, name, observed_child)
            # TODO: These are the modules that cannot be observed
            #       Once there are more, we should move them to a separate list
            if custom_module_class_mapping[type(child)] not in no_observer_set():
                insert_activation_post_process(observed_child)
        else:
            add_observer_(child, qconfig_propagation_list, non_leaf_module_list, device, custom_module_class_mapping)

    # Insert observers only for leaf nodes, note that this observer is for
    # the output of the module, for input QuantStub will observe them
    if len(module._modules) == 0 and not isinstance(module, torch.nn.Sequential) \
       and type(module) in qconfig_propagation_list:
        insert_activation_post_process(module)
