import sqlparse
from select_validator import *
from from_validator import *
from where_validator import *

def ValidateQuery(query):
    #Remove Duplicated Spaces and spaces from start and end
    query = " ".join(query.split())

    #check for empty string-------------------------
    length_query = len(query)
    if length_query == 0:
        return 'T', ''

    #Check for the ; in the end----------------------
    if query[length_query - 1] != ';':
        return 'Error: Invalid Syntax ; is not present', ''
    '''
    #Add space before ; if not present
    if(query[length_query - 2] != ' '):
        query = query[:length_query - 1] + ' ' + query[length_query - 1:]

    #Parsing query
    parsed_list = query.split()
    '''

    query = query.strip(';')
    query = sqlparse.format(query, keyword_case='upper')
    query = query.encode('UTF8')  #Encode query from Unicode

    query = query.split('FROM')
    length_query = len(query)

    #For valid query (length > 1) in all other cases invalid query
    if length_query <= 1:
        return 'Error: Invalid Syntax', ''

    #Check for 'SELECT' and elements between 'SELECT' and 'FROM'-------------------------
    result, select_query = SelectValidation(query)
    if result != True:
        return result, ''

    #Check for elements between 'FROM' and 'WHERE'--------------------------
    result, from_query = FromValidation(query)
    if result != True:
        return result, ''

    #Check for elements after 'WHERE'-------------------------------
    result, where_query = WhereValidation(query)
    if result != True:
        return result, ''

    parsed_list = [select_query, from_query, where_query]

    return True, parsed_list
