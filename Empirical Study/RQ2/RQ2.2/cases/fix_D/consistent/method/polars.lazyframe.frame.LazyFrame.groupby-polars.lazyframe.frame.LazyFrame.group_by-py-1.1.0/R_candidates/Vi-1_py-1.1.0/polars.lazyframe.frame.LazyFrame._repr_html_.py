    def _repr_html_(self) -> str:
        try:
            dot = self._ldf.to_dot(optimized=False)
            svg = subprocess.check_output(
                ["dot", "-Nshape=box", "-Tsvg"], input=f"{dot}".encode()
            )
            return (
                "<h4>NAIVE QUERY PLAN</h4><p>run <b>LazyFrame.show_graph()</b> to see"
                f" the optimized version</p>{svg.decode()}"
            )
        except Exception:
            insert = self.explain(optimized=False).replace("\n", "<p></p>")

            return f"""\
<i>naive plan: (run <b>LazyFrame.explain(optimized=True)</b> to see the optimized plan)</i>
    <p></p>
    <div>{insert}</div>\
"""
