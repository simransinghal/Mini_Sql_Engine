from helper import *
import sys

def execute_select(joinTable, select_query, from_query, require_tables):
    agg_func = ['MAX', 'MIN', 'SUM', 'AVG','DISTINCT','max','min','sum','avg','distinct']

    attr_dictionary = getHash(from_query, require_tables)

    flag = 0

    for func in agg_func:
        for q in select_query:
            if func in q:
                flag = 1

    if flag == 0:
        index = []
        if '*' in select_query:
            length = len(joinTable[0])
            for i in range(length):
                index.append(i)

        for q in select_query:
            if q in attr_dictionary:
                index.append(attr_dictionary[q])
            else:
                return False, []

        finalTable = [[row[i] for i in index] for row in joinTable]
        return True, finalTable

    else:
        m = {}
        flag = 0
        for q in select_query:
            for func in agg_func:
                if func in q:
                    m[q] = func
                    flag = 1

            if flag == 0:
                return False, []

        #Required columns from Select query
        col_index = []
        operation = []
        for x in select_query:
            op = x.split(')')
            if len(op) != 2:
                #Braces not balanced
                return False, []

            if '' not in op:
                #Case like Max(A)B
                return False, []

            op = op[0].split('(')
            if len(op) != 2:
                return False, []

            if op[1] not in attr_dictionary:
                return False, []

            col_index.append(attr_dictionary[op[1]])
            operation.append(op[0])

        temp_table = []
        for row in joinTable:
            temp = []
            for index in col:
                temp.append(row[index])
            temp_table.append(temp)

        #operations on column
        sumArr = [0]*len(col_index)
        distinctArr = [{}]*len(col_index)
        maxArr = []
        minArr = []
        for i in range(len(col_index)):
                maxArr.append(temp_table[0][i])
                minArr.append(temp_table[0][i])

        for row in temp_table:
            for i in range(len(col_index)):
                element = row[i]
                distinctArr[i][element] = 'a'
                sumArr[i] = sumArr[i] + int(element)
                maxArr[i] = max(maxArr[i], element)
                minArr[i] = min(minArr[i], element)

        N = 0
        for x in temp_table:
            N = N + 1

        for i in range(len(operation)):
            if operation[i] in ['SUM','sum']:
                finalTable.append(sumArr[i])
            elif operation[i] in ['AVG','avg']:
                finalTable.append(sumArr[i]/(N * 1.0))
            elif operation[i] in ['MAX', 'max']:
                finalTable.append(maxArr[i])
            elif operation[i] in ['MIN', 'min']:
                finalTable.append(minArr[i])
            elif operation[i] in ['DISTINCT', 'distinct']:
                finalTable = finalTable=list(distinctArr[i].keys())

    return True, finalTable
