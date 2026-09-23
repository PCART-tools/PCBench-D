    def __str__(self) -> str:
        return f"""\
naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)

{self.explain(optimized=False)}\
"""
