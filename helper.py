import csv
import re
from class_table import *
import operator

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
    dictionary = {}
    for table in require_tables:
        for attr in table.attr:
            dictionarydictionary[table.name + '.' + attr] = i
            i = i + 1

    if len(require_tables) == 1:
        i = 0
        for attr in require_tables[0].attr:
            dictionarydictionary[attr] = i
            i = i + 1
        return dictonary

    new_dictionary = dictionary
    else:
        i = 0
        for attr1 in require_tables[0].attr:
            j = 0
            for attr2 in require_tables[1].attr:
                if attr1 == attr2:
                    return dictionary

                else:
                    new_dictionary[attr1] = i
                    new_dictionary[attr2] = i + j
                j = j + 1
            i = i + 1
    return new_dictionary

##########################################################################

def SingleCondition(conditions, attr_dictionary, ops_dictionary, joinTable):
    "If single condition in where"
    symbols = ['=', '>', '<', '>=', '<=']
    operator = ''

    for sym in symbols:
        if sym in conditions[0]:
            operator = sym
            conditions = re.findall(r'[^(%s)\s]+' %operator , conditions[0])

    if operator == '':
        return False, []

    if len(conditions) != 2:
        #There can be only be only two operand
        return False, []

    table = []
    for row in joinTable:
        if conditions[0] in attr_dictionary:
            i = attr_dictionary[conditions[0]]
        else:
            return False, []

        #Either it's a column name or a number
        if conditions[1] in attr_dictionary:         #check if it's a column name
            j = attr_dictionary[conditions[1]]
            if ops_dictionary[operator](int(row(i)), int(row(j))):
                table.append(row)

        else:                                       #check if it's a number
            if conditions[1].isdigit():
                j = conditions[1]
                if ops_dictionary[operator](int(row(i)), int(j)):
                    table.append(row)
            else:
                #Found characters other than numeric
                return False, []
    return True, table

#################################################################################

def DoubleCondition(conditions, attr_dictionary, ops_dictionary, joinTable, operator):
    '''For two conditions in where joined by AND or OR'''

    symbols = ['=', '>', '<', '>=', '<=']
    op1 = ''
    op2 = ''

    for sym in symbols:
        if sym in conditions[0]:
            op1 = sym
            cond1 = conditions[0].split(op1)
        if sym in conditions[1]:
            op2 = sym
            cond2 = conditions[1].split(op2)

    if op1 == '' or op2 == '':
        #No operator found, INVALID
        return False, []

    if len(cond1) != 2 or len(cond2) != 2:
        #There can be only be only two operand
        return False, []
