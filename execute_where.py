from helper import *
import operator

def execute_where(joinTable, where_query, from_query, require_tables):

    rel_operator, conditions = GetOperator(where_query)

    if len(conditions) > 2:
        return False, []

    ops_dictionary = {'<': operator.lt, '<=': operator.le, '=':operator.eq, '>=':operator.ge, '>':operator.gt}
    attr_dictionary = getHash(from_query, require_tables)

    if len(conditions) == 1:
        result, table = SingleCondition(conditions, attr_dictionary, ops_dictionary, joinTable)
        if result != True:
            return result, []

    else:
        result, table = DoubleCondition(conditions, attr_dictionary, ops_dictionary, joinTable, rel_operator)
        if result != True:
            return result, []

    return True, table
