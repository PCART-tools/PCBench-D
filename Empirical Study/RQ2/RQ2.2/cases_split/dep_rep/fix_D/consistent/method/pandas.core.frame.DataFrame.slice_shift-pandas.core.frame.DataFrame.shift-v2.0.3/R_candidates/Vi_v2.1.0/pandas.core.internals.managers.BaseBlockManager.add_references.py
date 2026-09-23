    def add_references(self, mgr: BaseBlockManager) -> None:
        """
        Adds the references from one manager to another. We assume that both
        managers have the same block structure.
        """
        if len(self.blocks) != len(mgr.blocks):
            # If block structure changes, then we made a copy
            return
        for i, blk in enumerate(self.blocks):
            blk.refs = mgr.blocks[i].refs
            # Argument 1 to "add_reference" of "BlockValuesRefs" has incompatible type
            # "Block"; expected "SharedBlock"
            blk.refs.add_reference(blk)  # type: ignore[arg-type]
