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
        supported_modes = (
            "RGB",
            "RGBA",
            "RGBX",
            "CMYK",
            "I;16",
            "I;16L",
            "I;16B",
            "YCbCr",
            "LAB",
            "L",
            "1",
        )
        for mode in (input_mode, output_mode):
            if mode not in supported_modes:
                deprecate(
                    mode,
                    12,
                    {
                        "L;16": "I;16 or I;16L",
                        "L:16B": "I;16B",
                        "YCCA": "YCbCr",
                        "YCC": "YCbCr",
                    }.get(mode),
                )
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
