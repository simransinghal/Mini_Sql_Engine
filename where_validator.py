import re

def WhereValidation(query):

    #Splitting part between 'FROM' and 'WHERE'
    query = query[1].strip().split('WHERE')

    #Multiplle where are invalid
    if len(query) > 2:
        return False, ''

    if len(query) == 2:
        temp_query = query[1].strip().split(","); #split only about comma
        query = re.findall(r'[^,\s]+', query[1])  #split about both space and ','

        #Checking case "WHERE A = B,;"
        if '' in temp_query:
            return False,''

        return True, query

    else:
        return True, []
