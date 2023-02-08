def dict_to_tree_table(d: dict, table_name=None):
    """
    Convert dict to tree-table.

    See what is tree-table here:
    https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Tree-table
    """

    rd = {}
    for k, v in d.items():
        rd[k] = _get_rows_for_tree_table(v)

    return dict(
        type='treeTable',
        name=table_name,
        rows=rd
    )


def _get_rows_for_tree_table(d: dict, _list=False):
    """Protected recursive function for dict_to_tree_table function."""

    rd = {}
    if isinstance(d, dict):
        for k, v in d.items():
            rd[k] = _get_rows_for_tree_table(v)

        if _list:
            return rd
        else:
            return dict(
                type='collection',
                rows=rd
            )

    elif isinstance(d, list):
        rows = {}
        for idx, v in enumerate(d):
            rows[idx] = dict(
                type='collection',
                rows=_get_rows_for_tree_table(v, _list=True)
            )
        return dict(
            type='collection',
            rows=rows
        )

    elif isinstance(d, (str, int, float, tuple)) or d is None:
        if isinstance(d, tuple):
            columns = {F'col{idx}': v for idx, v in enumerate(d)}
        else:
            columns = {'col1': d}
        return dict(
            type='row',
            columns=columns
        )

    else:
        return _get_rows_for_tree_table(vars(d))
