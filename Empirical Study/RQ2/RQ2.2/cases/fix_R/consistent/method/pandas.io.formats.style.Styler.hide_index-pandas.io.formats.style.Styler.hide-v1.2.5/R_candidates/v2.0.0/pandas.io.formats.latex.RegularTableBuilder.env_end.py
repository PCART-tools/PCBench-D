    @property
    def env_end(self) -> str:
        return "\n".join(["\\end{tabular}", "\\end{table}"])
