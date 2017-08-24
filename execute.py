from class_table import *
from helper import *
from execute_where import *

def execute(parsed_list):
    select_query = parsed_list[0]
    from_query = parsed_list[1]
    where_query = parsed_list[2]

    table_list = getDB()
    result = ValidateTablename(from_query, table_list)
    if result == False:
        return False

    X, Y = GetTablesRows(from_query, table_list)

    if Y == []:
        joinTable = X

    else:
        joinTable = Join(X, Y)

    require_tables = []
    for tname in from_query:
        for t in table_list:
            if tname == t.name:
                require_tables.append(t)

    if where_query != []:
            result, joinTable = execute_where(joinTable, where_query, from_query, require_tables)
            if result == 'False':
                return False

    result, finalTable = execute_select(joinTable, select_query, from_query, require_tables)
    if result == False:
        return False

    printTable(finalTable, select_query)
    return 0                
