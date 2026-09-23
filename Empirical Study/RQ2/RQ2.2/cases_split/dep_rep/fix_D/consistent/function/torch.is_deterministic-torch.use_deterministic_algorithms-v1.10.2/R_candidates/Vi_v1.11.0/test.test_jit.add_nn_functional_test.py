def add_nn_functional_test(name, self_size, args, variant_name='', check_ad=(), skipTestIf=(),
                           output_process_fn=lambda x: x, kwargs=None):
    test_name = 'test_nn_' + name

    if variant_name != '':
        test_name = test_name + '_' + variant_name

    no_grad = variant_name == 'inplace'

    @suppress_warnings
    def do_test(self, name=name, args=args, test_name=test_name, check_ad=check_ad):
        torch.manual_seed(2)

        self_variable = create_input((self_size,))[0][0]

        # need to record this because methods can change the size (e.g. unsqueeze)
        args_variable, kwargs_variable = create_input(args, call_kwargs=kwargs)

        self_tensor = deepcopy(self_variable.data)
        args_tensor = deepcopy(unpack_variables(args_variable))

        if not no_grad:
            output_variable = getattr(F, name)(self_variable, *args_variable, **kwargs_variable)

        def fn(*inputs, **kwargs):
            return getattr(F, name)(*inputs, **kwargs)

        f_args_variable = (self_variable,) + args_variable
        f_args_tensor = (self_tensor,) + args_tensor
        should_autodiff_node, autodiff_nodes, fusible_nodes = normalize_check_ad(check_ad, name)

        if test_name not in EXCLUDE_SCRIPT:
            def run_test():
                # XXX: this test should always run with disable_autodiff_subgraph_inlining(True),
                #      so that we don't regress on autodiff support.
                with disable_autodiff_subgraph_inlining():
                    script_fn = create_script_fn(self, name, 'nn_functional')
                    check_against_reference(self, script_fn, fn, output_process_fn,
                                            f_args_variable, kwargs_variable, no_grad=no_grad)
                    # For tests we disabled AD subgraph inlining, make sure it's not falling back to autograd
                    if (doAutodiffCheck(test_name)):
                        self.assertAutodiffNode(script_fn.last_graph, should_autodiff_node, autodiff_nodes, fusible_nodes)

            if test_name in EXCLUDE_PYTHON_PRINT:
                with torch._jit_internal._disable_emit_hooks():
                    run_test()
            else:
                run_test()

    post_add_test(test_name, skipTestIf, do_test, TestJitGeneratedFunctional)
