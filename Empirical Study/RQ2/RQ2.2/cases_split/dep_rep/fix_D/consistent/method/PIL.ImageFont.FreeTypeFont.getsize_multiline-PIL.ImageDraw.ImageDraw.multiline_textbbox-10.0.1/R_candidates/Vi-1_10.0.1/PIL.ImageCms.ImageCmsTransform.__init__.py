    def __init__(
        self,
        input,
        output,
        input_mode,
        output_mode,
        intent=Intent.PERCEPTUAL,
        proof=None,
        proof_intent=Intent.ABSOLUTE_COLORIMETRIC,
        flags=0,
    ):
        if proof is None:
            self.transform = core.buildTransform(
                input.profile, output.profile, input_mode, output_mode, intent, flags
            )
        else:
            self.transform = core.buildProofTransform(
                input.profile,
                output.profile,
                proof.profile,
                input_mode,
                output_mode,
                intent,
                proof_intent,
                flags,
            )
        # Note: inputMode and outputMode are for pyCMS compatibility only
        self.input_mode = self.inputMode = input_mode
        self.output_mode = self.outputMode = output_mode

        self.output_profile = output
