from visions.functional import cast_to_inferred, detect_type, infer_type
from visions.typesets import StandardSet
import operator
import random
import pandas as pd 

typeset = StandardSet()

def Datatype(data):    
    data_type_sam = {}
    row=data.shape[0]
    data_sam = data.sample(int(row/10))
    #First Sample for the initialization of main dictionary
    for (columnName, columnData) in data_sam.iteritems():
        data_type_sam[columnName] = {str(infer_type(data_sam[columnName], typeset)):1}
    #Taking sample for 10 times for accuracy
    for i in range(9):
        data_sam = data.sample(int(row/10))
        for (columnName, columnData) in data_sam.iteritems():
            dataTypeValue = str(infer_type(data_sam[columnName], typeset))
            if data_type_sam[columnName].__contains__(dataTypeValue):
                data_type_sam[columnName][str(infer_type(data_sam[columnName], typeset))] += 1
            else:                
                data_type_sam[columnName][dataTypeValue] = 1

    data_type = {}

    #Making a dictionary with the datatype with maximum rate
    for (columnName, columnData) in data_sam.iteritems():
        max_value = max(data_type_sam[columnName].items(), key=operator.itemgetter(1))[0]
        data_type[columnName] = max_value

    return data_type

def changedt(data, data_type):
    change = []
    for (columnName, columnData) in data.iteritems():
        if data_type[columnName] ==  'DateTime':
            data_type_before = str(detect_type(data[columnName],typeset))
            data[columnName] = pd.to_datetime(data[columnName], errors = 'coerce')
            if data_type_before != str(detect_type(data[columnName],typeset)):
                print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_type(data[columnName],typeset)))
        elif (data_type[columnName] ==  'Integer') or (data_type[columnName] ==  'Float'):
                data_type_before = str(detect_type(data[columnName],typeset))
                data[columnName] = pd.to_numeric(data[columnName], errors = 'coerce')
                if data_type_before != str(detect_type(data[columnName],typeset)):
                    print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_type(data[columnName],typeset)))
        elif data_type[columnName] ==  'TimeDelta':
            data_type_before = str(detect_type(data[columnName],typeset))
            data[columnName] = pd.to_timedelta(data[columnName], errors = 'coerce')
            if data_type_before != str(detect_type(data[columnName],typeset)):
                print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_type(data[columnName],typeset)))
        else:
            data[columnName] = data[columnName]

    return data

def findnull(data):
    #Finding the number of missing data
    before = data.shape[0]
    data_copy = data.copy()
    data_copy.dropna(inplace = True)
    after = data_copy.shape[0]
    null_data = before - after
    return null_data,before