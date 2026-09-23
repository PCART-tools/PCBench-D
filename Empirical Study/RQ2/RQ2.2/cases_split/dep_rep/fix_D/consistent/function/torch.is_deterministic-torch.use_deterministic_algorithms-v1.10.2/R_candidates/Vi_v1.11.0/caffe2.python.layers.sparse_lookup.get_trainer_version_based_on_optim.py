def get_trainer_version_based_on_optim(optim_def):
    if isinstance(optim_def, Optimizer) and hasattr(optim_def, "engine"):
        logger.info(
            "Attempting to set trainer version for engine {}".format(optim_def.engine)
        )
        if optim_def.engine in FP16_ENGINES:
            logger.info("Setting FP16 trainer for engine {}".format(optim_def.engine))
            return "fp16"
        else:
            logger.info("Setting FP32 trainer for engine {}".format(optim_def.engine))
            return "fp32"
    else:
        return "fp32"
