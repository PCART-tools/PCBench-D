    def _deprecate_downcast(self, downcast, method_name: str):
        # GH#40988
        if downcast is not lib.no_default:
            warnings.warn(
                f"The 'downcast' keyword in {method_name} is deprecated and "
                "will be removed in a future version. Use "
                "res.infer_objects(copy=False) to infer non-object dtype, or "
                "pd.to_numeric with the 'downcast' keyword to downcast numeric "
                "results.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
        else:
            downcast = None
        return downcast
