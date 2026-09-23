    async def forward(self, inputs=Body(None, embed=True)):
        """
        **inputs**:
        **attention_mask**:
        **tokens_type_ids**:
        """

        # Check we don't have empty string
        if len(inputs) == 0:
            return ServeForwardResult(output=[], attention=[])

        try:
            # Forward through the model
            output = self._pipeline(inputs)
            return ServeForwardResult(output=output)
        except Exception as e:
            raise HTTPException(500, {"error": str(e)})
