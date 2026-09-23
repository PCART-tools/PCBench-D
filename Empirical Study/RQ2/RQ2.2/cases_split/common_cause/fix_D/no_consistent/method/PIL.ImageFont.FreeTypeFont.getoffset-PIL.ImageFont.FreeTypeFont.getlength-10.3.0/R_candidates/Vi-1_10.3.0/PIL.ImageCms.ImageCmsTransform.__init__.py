    def __init__(
        self,
        input: ImageCmsProfile,
        output: ImageCmsProfile,
        input_mode: str,
        output_mode: str,
        intent: Intent = Intent.PERCEPTUAL,
        proof: ImageCmsProfile | None = None,
        proof_intent: Intent = Intent.ABSOLUTE_COLORIMETRIC,
        flags: Flags = Flags.NONE,
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
