    def _remove_unused_columns(self, dataset: "datasets.Dataset", description: Optional[str] = None):
        if not self.args.remove_unused_columns:
            return
        # Inspect model forward signature to keep only the arguments it accepts.
        signature = inspect.signature(self.model.forward)
        signature_columns = list(signature.parameters.keys())
        # Labels may be named label or label_ids, the default data collator handles that.
        signature_columns += ["label", "label_ids"]
        columns = [k for k in signature_columns if k in dataset.column_names]
        ignored_columns = list(set(dataset.column_names) - set(signature_columns))
        dset_description = "" if description is None else f"in the {description} set "
        logger.info(
            f"The following columns {dset_description}don't have a corresponding argument in `{self.model.__class__.__name__}.forward` and have been ignored: {', '.join(ignored_columns)}."
        )
        dataset.set_format(type=dataset.format["type"], columns=columns)
