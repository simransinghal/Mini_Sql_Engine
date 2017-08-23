from helper import *

def execute_where(joinTable, where_query, from_query, require_tables):

    operator, conditions = GetOperator(where_query)

    if len(conditions) > 2:
        return False

    relational_ops = {'<': operator.lt, '<=': operator.le, '=':operator.eq, '>=':operator.ge, '>':operator.gt}

    h = getHash(from_query, require_tables)

    if len(conditions) == 1:
                SingleCondition(conditions, h, relational_ops, joinTable)
