
import sys
from validator import *

if __name__ == "__main__":

    while 1:
        query = raw_input("\nmysql> ")

        if query == 'q' or query == 'quit':
            sys.exit()

        result, parsed_list = ValidateQuery(query)
        if result == False:
            print "Error"
            continue

        #Execute commands, which are syntatically parsed
        execute(parsed_list)
            
