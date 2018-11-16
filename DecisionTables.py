#this is PyDT - Python Decision Tables
# (c) 2007 Michael Neale (michael@michaelneale.net)
# Use entirely at your own risk !
# Licenced under LGPL unless stated otherwise


import xlrd
from functools import reduce
#this is the actual "engine" if you can call it that.
def process_dt(fact, table) :
    #calc the headers
    def make_header(hdr) :
        splut = hdr[1].split(' ')
        if len(splut) > 1 :
            return [hdr[0], fact[splut[0]] + ' ' + splut[1]]
        else :
            return [hdr[0], fact[hdr[1]]]
    headers = list(map(make_header, table['condition_headers']))
    #lets try a map based approach
    def eval_table(row) :
        #go through all the conditions, evaluating
        def check_condition(condition) :
            col_index = condition[0]
            if not col_index in row :
                return False
            cell_value = row[col_index]
            predicate = str(condition[1]) + str(cell_value)
            return eval(predicate)
        allTrue = lambda a, b : a and b
        check_result = reduce(allTrue, list(map(check_condition,headers)))
        if check_result :
            #for action in table['action_headers'] :
            def apply_actions(action) :
                col_label = action[0]
                if (col_label in row) :
                    fact[action[1]] = row[col_label]
            list(map(apply_actions, table['action_headers']))
    list(map(eval_table, table['data'])),

# Load a XLS into a decision table structure for processing
def load_xls(file_name) :
    book = xlrd.open_workbook(file_name)
    sh = book.sheet_by_index(0)	
    condition_headers, action_headers, data = [],[],[]
    for rx in range(sh.nrows):
            if rx == 0 :		
                    divider = 0
                    for cx in range(sh.ncols):
                            cv = sh.cell_value(rowx=rx, colx=cx)				
                            if cv == "" : 
                                    continue
                            if cv == "*" or cv == 'actions:' :
                                    divider = cx
                            else:
                                    if divider == 0 : #we are in conditions
                                            condition_headers.append([cx, cv])
                                    else: #we are in actions
                                            action_headers.append([cx, cv])
            else:	
                    data_row = {}
                    #print condition_headers
                    for cx in range(sh.ncols):
                            cv = sh.cell_value(rowx=rx, colx=cx)
                            if cv != "":
                                    data_row[cx] = cv
                    if len(data_row) > 0 :
                            data.append(data_row)
    return {
            "condition_headers" : condition_headers,
            "action_headers" : action_headers,
            "data" : data
            }




