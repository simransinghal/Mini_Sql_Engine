import re

def FromValidation(query):

    #Check if any element after 'FROM' in query eg. (SELECT * FROM)
    if query[1] == '':
        return 'Error: Invalid Syntax near FROM', ''

    #Splitting part between 'FROM' and 'WHERE'
    query = query[1].strip().split('WHERE')

    #Checking "FROM A B " without comma invalid
    if ',' not in query[0] and len(query[0].strip().split()) > 1:
        return 'Error: Invalid Syntax "," needed', ''

    #Checking case when "FROM WHERE " without table name invalid
    if len(query[0].strip().split()) == 0:
        return 'Error: Invalid Syntax near FROM',''

    temp_query = query[0].strip().split(","); #split only about comma
    query = re.findall(r'[^,\s]+', query[0])  #split about both space and ','

    #Checking case "FROM A, B, WHERE"
    if '' in temp_query:
        return 'Error: Invalid Syntax near "," ' , ''

    if(len(query) > 2):
        return 'Error: Invalid Syntax, max table lenth = 2', ''

    return True, query
