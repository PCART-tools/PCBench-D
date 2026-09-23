    def return_insert_id(self):
        return "RETURNING %s INTO %%s", (InsertIdVar(),)
