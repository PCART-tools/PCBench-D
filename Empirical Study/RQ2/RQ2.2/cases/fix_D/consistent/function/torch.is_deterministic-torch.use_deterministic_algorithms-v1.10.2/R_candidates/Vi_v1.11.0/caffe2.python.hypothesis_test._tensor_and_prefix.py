@st.composite
def _tensor_and_prefix(draw, dtype, elements, min_dim=1, max_dim=4, **kwargs):
    dims_ = draw(
        st.lists(hu.dims(**kwargs), min_size=min_dim, max_size=max_dim))
    extra_ = draw(
        st.lists(hu.dims(**kwargs), min_size=min_dim, max_size=max_dim))
    assume(len(dims_) + len(extra_) < max_dim)
    return (draw(hu.arrays(dims_ + extra_, dtype, elements)),
            draw(hu.arrays(extra_, dtype, elements)))
