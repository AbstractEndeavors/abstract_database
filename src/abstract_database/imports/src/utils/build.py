from .imports import sql
def get_table_name(tableName,schema='public'):
    return sql.SQL('{}.{}').format(
        sql.Identifier(schema),
        sql.Identifier(tableName)
        )
def map_parts_vals(data_map,vals=None,any_value=False):
    """
    Returns: (sql.SQL fragment, values list)
    """
    parts, vals = [], vals or []
    for col, val in data_map.items():
        s_value = "{} = %s"
        if any_value:
            s_value = "{} = ANY(%s)"
        parts.append(sql.SQL(s_value).format(sql.Identifier(col)))
        vals.append(val)
    return parts, vals
def build_set_clause(data_map,vals=None,any_value=False):
    parts, vals = map_parts_vals(
        data_map=data_map,
        vals=vals,
        any_value=any_value
        )
    parts = sql.SQL(', ').join(parts)
    return parts, vals

def build_return_clause(returning = None):
    qry = sql.SQL('')
    if returning:
        if returning is True:
            qry += sql.SQL(' RETURNING *')
        elif returning == 'count':
            qry = sql.SQL("WITH upd AS (") + qry + sql.SQL(" RETURNING 1) SELECT COUNT(*) FROM upd")
        else:
            cols = [c.strip() for c in returning.split(',')]
            columns = [sql.Identifier(c) for c in cols]
            qry += sql.SQL(' RETURNING ') + sql.SQL(', ').join(columns)
    return qry 
def build_where_clause(filter_map=None, vals=None, any_value=False):
    """
    Returns: (sql.SQL fragment starting with ' WHERE …' or sql.SQL(''), values list)
    """
    parts = sql.SQL('')
    values = vals or []
    if filter_map:
        parts, vals = map_parts_vals(
            data_map=filter_map,
            vals=values,
            any_value=any_value
            )
        parts = sql.SQL(' WHERE ') + sql.SQL(' AND ').join(parts)
    return parts , vals

def select_column_names(column_names,count=False):
    select_cols = None
    # SELECT list
    if count:
        select_cols = sql.SQL("COUNT(*)")
    elif column_names == '*':
        select_cols = sql.SQL('*')
    elif isinstance(column_names,str):
        column_names = [c.strip() for c in column_names.split(',')]
    if isinstance(column_names,list) and select_cols is None:
        select_cols = sql.SQL(', ').join(sql.Identifier(c) for c in column_names)
    return select_cols
def get_value_from_row(row):
    if isinstance(row,list):
        for i,item in enumerate(row):
            if isinstance(item,dict):
                item = list(item.values())
            row[i] = item[0]
    if isinstance(row,dict):
        row = list(row.values())
        row = row[0]
    if isinstance(row,list) and len(row) == 1:
        row = row[0]
    return row
