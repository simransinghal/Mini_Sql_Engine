import re

#Select validator
def SelectValidation(query):
    temp_query = query[0].strip().split(" ",1) #Only 1st space is split
    query = re.findall(r'[^,\s]+', query[0])  #split about both space and ','

    #check first element of list is 'SELECT' or not

    if len(query) > 0 and query[0] != 'SELECT':
        return 'Error: Invalid Syntax "SELECT" not present' , ''

    #Check if any column is present in query
    if len(query) <= 1:
        return 'Error: Invalid Syntax', ''

    for i in range(len(query)):
        #Detecting queries like *col1 (forgot ',' in between * and col1)
        if '*' in query[i] and len(query[i]) > 1:
            return 'Error: Invalid Syntax "," not present', ''

        #'*' can not be present at any other place like "Select col1, * from Table1"
        if '*' in query[i] and i != 1:
            return 'Error: Invalid Syntax near *', ''

    temp_query = temp_query[1].strip().split(",");  #Splitting column names about ','

    #Detecting case like 'Select abc, pr, from' or 'Select *, from'
    if '' in temp_query:
        return 'Error: Invalid Syntax near ","', ''

    query.pop(0)
    return True, query
