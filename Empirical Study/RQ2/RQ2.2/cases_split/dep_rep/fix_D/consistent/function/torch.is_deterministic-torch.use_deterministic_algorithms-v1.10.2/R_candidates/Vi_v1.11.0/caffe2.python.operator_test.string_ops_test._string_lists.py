def _string_lists(alphabet=None):
    return st.lists(
        elements=st.text(alphabet=alphabet) if alphabet else st.text(),
        min_size=0,
        max_size=3)
