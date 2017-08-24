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
            return "Error: table does not exist"

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
    '''for row1 in X:
        for row2 in Y:
            joinTable.append(row1 + row2)
    '''
    for row2 in Y:
        for row1 in X:
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
            dictionary[table.name + '.' + attr] = i
            i = i + 1

    if len(require_tables) == 1:
        i = 0
        for attr in require_tables[0].attr:
            dictionary[attr] = i
            i = i + 1
        return dictionary

    else:

        temp = []
        for attr1 in require_tables[0].attr:
            for attr2 in require_tables[1].attr:
                if attr1 == attr2:
                    temp.append(attr1)

        if temp == []:
            return dictionary

        i = 0
        for attr1 in require_tables[0].attr:
            if attr1 not in temp:
                dictionary[attr1] = i;
            i = i + 1

        j = 0
        for attr2 in require_tables[1].attr:
            if attr2 not in temp:
                dictionary[attr2] = len(require_tables[0].attr) + j
            j = j + 1

    return dictionary

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
        return "Error: Valid Operator does not exist", []

    '''
    if i != 1:
        #There can be only be only two operand
        return "Error: Invalid Syntax in condition", []
    '''

    table = []
    for row in joinTable:
        if conditions[0] in attr_dictionary:
            i = attr_dictionary[conditions[0]]
        else:
            return "Error: Attribute does not exist", []

        #Either it's a column name or a number
        if conditions[1] in attr_dictionary:         #check if it's a column name
            j = attr_dictionary[conditions[1]]

            if ops_dictionary[operator](int(row[i]), int(row[j])):
                table.append(row)

        else:                               #check if it's a number
            if conditions[1].isdigit():
                j = conditions[1]
                if ops_dictionary[operator](int(row[i]), int(j)):
                    table.append(row)
            else:
                #Found characters other than numeric
                return "Error: Invalid operand", []
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
        return "Error: Valid Operator does not exist", []

    '''if i != 1 or j != 1:
        #There can be only be only two operand
        return "Error: Invalid Syntax in condition", []
    '''

    table = []
    for row in joinTable:
        if cond1[0] in attr_dictionary and cond2[0] in attr_dictionary:
            i1 = attr_dictionary[cond1[0]]
            i3 = attr_dictionary[cond2[0]]
        else:
            return "Error: Attribute does not exist", []

        if cond1[1] in attr_dictionary:
            i2 = attr_dictionary[cond1[1]]
            val1 = ops_dictionary[op1](int(row[i1]), int(row[i2]))
        elif cond1[1].isdigit():
            i2 = cond1[1]
            val1 = ops_dictionary[op1](int(row[i1]), int(i2))
        else:
            return "Error: Invalid operand", []

        if cond2[1] in attr_dictionary:
            i4 = attr_dictionary[cond2[1]]
            val2 = ops_dictionary[op2](int(row[i3]), int(row[i4]))

        elif cond2[1].isdigit():
            i4 = cond2[1]
            val2 = ops_dictionary[op2](int(row[i3]), int(i4))
        else:
            return "Error: Invalid operand", []

        if operator == 'AND':
            if val1 and val2:
                table.append(row)
        else:
            if val1 or val2:
                table.append(row)

    return True, table

###################################################################################

def printTable(finalTable, select_query, require_tables):
    for q in select_query:
        if 'distinct' in q or 'DISTINCT' in q or 'Distinct' in q:
            print select_query[0]
            for element in finalTable:
                print element
            return

    temp = []
    if '*' in select_query:
        if len(require_tables) > 1:

            for i in range(len(require_tables[0].attr)):
                require_tables[0].attr[i] = require_tables[0].name + '.' + require_tables[0].attr[i]

            for i in range(len(require_tables[1].attr)):
                require_tables[1].attr[i] = require_tables[1].name + '.' + require_tables[1].attr[i]

            temp = require_tables[0].attr + require_tables[1].attr

        if len(require_tables) == 1:

            for i in range(len(require_tables[0].attr)):
                require_tables[0].attr[i] = require_tables[0].name + '.' + require_tables[0].attr[i]

            temp = require_tables[0].attr

    else :
        for q in select_query:
            temp.append(q)

    print(" ".join([element for element in temp]))

    for row in finalTable:
        #print row
        if isinstance(row,list):
            print (" ".join([element for element in row]))
        else:
            print row
