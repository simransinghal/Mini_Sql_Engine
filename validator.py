import sqlparse

def ValidateQuery(query):

    #Remove Duplicated Spaces and spaces from start and end
    query = " ".join(query.split())

    #check for empty string-------------------------
    length_query = len(query)
    if length_query == 0:
        return False

    #Check for the ; in the end----------------------
    if query[length_query - 1] != ';':
        return False
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
        return False

        



    print query
