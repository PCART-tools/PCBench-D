def run_model(
    model_base, model_control, model_input, num_iterations=10, precision=1e-4
):
    clean_memory()
    for i in range(num_iterations):
        logger.info("start %s iteration", i)
        set_deterministic()
        pred_base = model_base(*model_input)
        set_deterministic()
        pred_control = model_control(*model_input)

        res = compare_parameters(model_base, model_control, precision)
        logger.info("compare parameters. Numerical result : %s", res)

        res = compare_forward_output(pred_base, pred_control, precision)
        logger.info("compare loss/predict. Numerical result : %s", res)
        # tensor may not have a grad_fn
        try:
            _ = pred_base[0].sum().backward(retain_graph=True)
            _ = pred_control[0].sum().backward(retain_graph=True)
            res = compare_gradients(model_base, model_control, precision)
            logger.info("compare param grad. Numerical result : %s", res)
        except Exception:
            logger.exception("Exception when comparing gradients")
            traceback.print_exc()

        if config.fx_passes_numeric_check["requires_optimizer"]:
            try:
                optimizer_base = optim.SGD(
                    [param for name, param in model_base.named_parameters()], lr=0.01
                )
                optimizer_base.step()

                optimizer_control = optim.SGD(
                    [param for name, param in model_control.named_parameters()], lr=0.01
                )
                optimizer_control.step()

                res = compare_parameters(model_base, model_control, precision)
                logger.info(
                    "compare parameters with optimizer added. Numerical result : %s",
                    res,
                )
            except Exception:
                logger.exception(
                    "Exception when optimizer is added to check parameter names"
                )
                traceback.print_exc()
        else:
            logger.warning(
                "no parameter with optimizer to compare with length %s before transformation"
                " and the length %s after transformation",
                len(dict(model_base.named_parameters())),
                len(dict(model_control.named_parameters())),
            )
