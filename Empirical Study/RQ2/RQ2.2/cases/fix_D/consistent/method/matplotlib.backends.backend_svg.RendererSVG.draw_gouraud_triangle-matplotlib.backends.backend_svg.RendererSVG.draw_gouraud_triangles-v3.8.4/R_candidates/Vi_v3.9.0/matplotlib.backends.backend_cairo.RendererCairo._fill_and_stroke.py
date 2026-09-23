    @staticmethod
    def _fill_and_stroke(ctx, fill_c, alpha, alpha_overrides):
        if fill_c is not None:
            ctx.save()
            _set_rgba(ctx, fill_c, alpha, alpha_overrides)
            ctx.fill_preserve()
            ctx.restore()
        ctx.stroke()
