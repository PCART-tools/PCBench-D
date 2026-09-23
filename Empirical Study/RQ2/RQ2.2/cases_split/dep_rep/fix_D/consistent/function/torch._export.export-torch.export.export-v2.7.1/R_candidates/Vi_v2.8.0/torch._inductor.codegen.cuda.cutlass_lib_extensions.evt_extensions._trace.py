    def _trace(
        fn_src: str, example_tensors: dict[str, CutlassTensor], cc: int, **kwargs: Any
    ) -> EpilogueFunctor:
        class EpilogueFunctor(PythonASTFrontend):
            def __init__(self, cc: int, **kwargs: Any):
                self.source = textwrap.dedent(fn_src)
                super().__init__(cc, **kwargs)

            def parse(self, example_inputs: dict[str, CutlassTensor]) -> None:
                self.example_inputs = example_inputs
                self.ast = ast.parse(self.source)
                self.visit(self.ast)

        cc = int(cuda_env.get_cuda_arch())
        epilogue_functor = EpilogueFunctor(cc=cc, **kwargs)
        epilogue_functor.trace(example_tensors)
        return epilogue_functor
