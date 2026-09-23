    def save_vocabulary(self, save_directory: str) -> Tuple[str]:
        """save vocab file to json and copy spm files from their original path."""
        save_dir = Path(save_directory)
        assert save_dir.is_dir(), f"{save_directory} should be a directory"
        save_json(self.encoder, save_dir / self.vocab_files_names["vocab"])

        for orig, f in zip(["source.spm", "target.spm"], self.spm_files):
            dest_path = save_dir / Path(f).name
            if not dest_path.exists():
                copyfile(f, save_dir / orig)

        return tuple(save_dir / f for f in self.vocab_files_names)
