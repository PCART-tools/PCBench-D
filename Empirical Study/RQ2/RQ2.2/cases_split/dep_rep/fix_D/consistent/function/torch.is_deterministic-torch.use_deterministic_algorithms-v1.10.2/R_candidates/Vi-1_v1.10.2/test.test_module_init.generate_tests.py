def generate_tests(test_cls, constructor_arg_db):
    # test all modules underneath these namespaces...
    NAMESPACES = [
        torch.nn,
        torch.nn.qat,
        torch.nn.quantizable,
        torch.nn.quantized,
    ]
    # ...except these
    MODULES_TO_SKIP = {
        torch.nn.Module,
        torch.nn.Container,  # deprecated
        torch.nn.NLLLoss2d,  # deprecated
        torch.nn.quantized._ConvNd,  # base class in __all__ for some reason
        # TODO: Remove these 2 from this list once the ASan issue is fixed.
        # See https://github.com/pytorch/pytorch/issues/55396
        torch.nn.quantized.Embedding,
        torch.nn.quantized.EmbeddingBag,
    }
    # no need to support kwargs for these modules even though
    # they have parameters / buffers because they are passed in
    # already instantiated
    MODULES_WITHOUT_KWARGS_SUPPORT = {
        torch.nn.BCELoss,
        torch.nn.BCEWithLogitsLoss,
        torch.nn.CrossEntropyLoss,
        torch.nn.FractionalMaxPool2d,
        torch.nn.FractionalMaxPool3d,
        torch.nn.MultiLabelSoftMarginLoss,
        torch.nn.MultiMarginLoss,
        torch.nn.NLLLoss,
        torch.nn.TransformerDecoder,
        torch.nn.TransformerEncoder,
    }
    # modules that supported kwargs before
    MODULES_WITH_PREVIOUS_KWARGS = {
        torch.nn.Identity,
    }
    # lazy modules don't instantiate parameters right away
    LAZY_MODULES = {
        torch.nn.LazyBatchNorm1d,
        torch.nn.LazyBatchNorm2d,
        torch.nn.LazyBatchNorm3d,
        torch.nn.LazyConv1d,
        torch.nn.LazyConv2d,
        torch.nn.LazyConv3d,
        torch.nn.LazyConvTranspose1d,
        torch.nn.LazyConvTranspose2d,
        torch.nn.LazyConvTranspose3d,
        torch.nn.LazyConvTranspose3d,
        torch.nn.LazyInstanceNorm1d,
        torch.nn.LazyInstanceNorm2d,
        torch.nn.LazyInstanceNorm3d,
        torch.nn.LazyLinear,
    }
    # these modules requires FBGEMM backend to instantiate
    MODULES_THAT_REQUIRE_FBGEMM = {
        torch.nn.quantized.Conv1d,
        torch.nn.quantized.Conv2d,
        torch.nn.quantized.Conv3d,
        torch.nn.quantized.ConvTranspose1d,
        torch.nn.quantized.ConvTranspose2d,
        torch.nn.quantized.ConvTranspose3d,
        torch.nn.quantized.Linear,
    }

    for namespace in NAMESPACES:
        # the "nn" in "torch.nn"
        namespace_basename = namespace.__name__.split('.')[-1]
        for module_name in namespace.modules.__all__:
            # class object for this module (e.g. torch.nn.Linear)
            module_cls = getattr(namespace.modules, module_name)
            if module_cls in MODULES_TO_SKIP:
                continue
            verify_kwargs = module_cls not in MODULES_WITHOUT_KWARGS_SUPPORT
            module_is_lazy = module_cls in LAZY_MODULES
            check_nonexistent_arg = module_cls not in MODULES_WITH_PREVIOUS_KWARGS
            # Generate a function for testing this module and setattr it onto the test class.
            run_test = generate_test_func(test_cls, module_cls, constructor_arg_db,
                                          verify_kwargs=verify_kwargs,
                                          module_is_lazy=module_is_lazy,
                                          check_nonexistent_arg=check_nonexistent_arg)
            test_name = f'test_{namespace_basename}_{module_name}'
            if module_cls in MODULES_THAT_REQUIRE_FBGEMM:
                run_test = skipIfNoFBGEMM(run_test)
            setattr(TestModuleInit, test_name, run_test)
