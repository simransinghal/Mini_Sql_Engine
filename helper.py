import csv
from class_table import *

def getDB():
    table_list = []
    with open('metadata.txt', 'r') as f:
        check = 0
        attr = []
        table_name = ''
        file_name = ''
        for line in f:
            line = line.strip()
            if line == '<end_table>':
                table = []
                with open(file_name, 'rb') as csvfile:
                    content = csv.reader(csvfile, delimiter = ',')
                    for row in content:
                        table.append(row)

                table_list.append(Table(table_name, attr, table))
                attr = []
                check = 0

            elif check == 0:
                check = 1

            elif check == 1:
                table_name = line
                file_name = table_name + '.csv'
                check = 2

            else:
                attr.append(line)
    return table_list

########################################################################

def ValidateTablename(from_query, table_list):
    for f in from_query:
        found = 0
        for table in table_list:
            if f == table.name:
                found = 1
                break
        if found == 0:
            return False

    return True

##############################################################################

def GetTablesRows(from_query, table_list):
    X = []
    Y = []
    for t in table_list:
        if from_query[0] == t.name:
            X = t.table
        if len(from_query) > 1 and from_query[1] == t.name:
            Y = t.table
    return X, Y

###############################################################################

def Join(X, Y):
    joinTable = []
    for row1 in X:
        for row2 in Y:
            joinTable.append(row1 + row2)
    return joinTable

##############################################################################

def GetOperator(where_query):
    #Get the operator in where and parse it
    operator = ''
    if 'AND' in where_query:
        index = where_query.index('AND')
        operator = 'AND'
    elif 'OR' in where_query:
        index = where_query.index('OR')
        operator = 'OR'
    else:
        index = -1

    if operator != '':
        q1 = ''.join(where_query[0:index])
        q2 = ''.join(where_query[index + 1:])
        conditions = [q1, q2] #query

    else:
        q = ''.join(where_query)
        conditions = [q]

    return operator, conditions

############################################################################

def getHash(from_query, require_tables):
    i = 0
    dictonary = {}
    for table in require_tables:
        for attr in table.attr:
            dictonary[table.name + '.' + attr] = i
            i = i + 1
##########################################################################

def SingleCondition(conditions, h, relational_ops, joinTable):
    "If single condition in where"
    symbols = ['=', '>', '<', '>=', '<=']
    operator = ''

    for sym in symbols:
        if sym in conditions[0]:
            operator = sym
            split_condition = conditions[0].split(operator)
            
