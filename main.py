
import sys
from validator import *
from execute import *
from termcolor import colored

if __name__ == "__main__":

    while 1:
        query = raw_input(colored("mysql> ", 'green'))

        if query.upper() == 'Q' or query.upper() == 'QUIT':
            sys.exit()

        result, parsed_list = ValidateQuery(query)
        if result != True and result != 'T':
            print colored(result, 'red')
            continue
        elif result == 'T':             #If empty string continue
            continue

        #Execute commands, which are syntatically parsed
        result = execute(parsed_list)
        if result != True:
            print colored(result, 'red')
