from helper import *
import sys

def execute_select(joinTable, select_query, from_query, require_tables):
    agg_func = ['MAX', 'MIN', 'SUM', 'AVG','DISTINCT','max','min','sum','avg','distinct','Max','Min', 'Sum','Avg','Distinct']

    attr_dictionary = getHash(from_query, require_tables)

    if '*' in select_query:
        return True, joinTable

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
                return "Error: Attribute does not exist", []

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
                return "Error: Invalid Syntax", []

        #Required columns from Select query
        col_index = []
        operation = []
        for x in select_query:
            op = x.split(')')
            if len(op) != 2:
                #Braces not balanced
                return "Error: Improper Braces", []

            if '' not in op:
                #Case like Max(A)B
                return "Error: Invalid Syntax", []

            op = op[0].split('(')
            if len(op) != 2:
                return "Error: Improper Braces", []

            if op[1] not in attr_dictionary:
                return "Error: Attribute does not exist", []

            col_index.append(attr_dictionary[op[1]])
            operation.append(op[0])

        temp_table = []
        for row in joinTable:
            temp = []
            for index in col_index:
                temp.append(row[index])
            temp_table.append(temp)

        #operations on column
        sumArr = [0]*len(col_index)
        distinctArr = [[]]*len(col_index)
        maxArr = []
        minArr = []
        for i in range(len(col_index)):
                maxArr.append(temp_table[0][i])
                minArr.append(temp_table[0][i])

        for row in temp_table:
            for i in range(len(col_index)):
                element = row[i]
                #distinctArr[i][int(element)] = 'a'
                if element not in distinctArr[i]:
                    distinctArr[i].append(element)
                sumArr[i] = sumArr[i] + int(element)
                maxArr[i] = max(int(maxArr[i]), int(element))
                minArr[i] = min(int(minArr[i]), int(element))

        N = 0
        for x in temp_table:
            N = N + 1

        Distinct_present = 'NO'
        Any_other = 'NO'
        for i in range(len(operation)):
            if operation[i] in ['DISTINCT', 'distinct','Distinct']:
                Distinct_present = 'YES'
            else:
                Any_other = 'YES'

        if Distinct_present == 'YES' and Any_other == 'YES':
            return 'Error: Distinct can not be used with other functions', []

        if Distinct_present == 'YES' and Any_other == 'NO':
            finalTable = []
            for i in range(len(operation)):
                if i == 0:
                    finalTable = distinctArr[i]
                else:
                    temp = []
                    for j in range(len(distinctArr[i])):
                        if distinctArr[i][j] not in finalTable:
                            temp.append(distinctArr[i][j])
                    finalTable = finalTable + temp        
            return True,finalTable

        finalTable = []
        for i in range(len(operation)):
            if operation[i] in ['SUM','sum','Sum']:
                finalTable.append(sumArr[i])
            elif operation[i] in ['AVG','avg','Avg']:
                finalTable.append(sumArr[i]/(N * 1.0))
            elif operation[i] in ['MAX', 'max','Max']:
                finalTable.append(maxArr[i])
            elif operation[i] in ['MIN', 'min','Min']:
                finalTable.append(minArr[i])
            elif operation[i] in ['DISTINCT', 'distinct','Distinct']:
                finalTable = distinctArr[i]

    return True, finalTable
