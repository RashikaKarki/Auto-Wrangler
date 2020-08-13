import os
import operator
import random
import pandas as pd 
import numpy as np
from pandas import json_normalize
import json
import io
from visions.functional import detect_series_type, infer_series_type
from visions.typesets import StandardSet
import seaborn as sb
sb.set_palette('Set2')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


typeset = StandardSet()
typeset.types


def has_header(data,data_nohead,nrows=20):
    data1 = data_nohead.head(nrows)
    data2 = data.head(nrows)
    return (tuple(data1.dtypes) != tuple(data2.dtypes))

def Main_func(data, data_nohead):

    #Checking Header

    hasheader = has_header(data,data_nohead)
    feature_rename = []
    if hasheader == False:
        total = data.shape[1]
        for i in range(total):
            columnNumber = i + 1
            x = "Enter the name of column " +  str(columnNumber) +": "
            nameInput = input(x)
            feature_rename.append(str(nameInput))
        data.columns=feature_rename

    flag = 0
    #Handling Datatype

    if flag == 0:
      
        data_type_sam = {}
        row=data.shape[0]
        data_sam = data.sample(int(row/10))

        #First Sample for the initialization of main dictionary
        for (columnName, columnData) in data_sam.iteritems():

            data_type_sam[columnName] = {str(infer_series_type(data_sam[columnName], typeset)):1}

        #Taking sample for 10 times for accuracy
        for i in range(9):

            data_sam = data.sample(int(row/10))

            for (columnName, columnData) in data_sam.iteritems():

                dataTypeValue = str(infer_series_type(data_sam[columnName], typeset))

                if data_type_sam[columnName].__contains__(dataTypeValue):

                    data_type_sam[columnName][str(infer_series_type(data_sam[columnName], typeset))] += 1

                else:
                    
                    data_type_sam[columnName][dataTypeValue] = 1


            data_type = {}

    
        #Making a dictionary with the datatype with maximum rate
        for (columnName, columnData) in data_sam.iteritems():

            max_value = max(data_type_sam[columnName].items(), key=operator.itemgetter(1))[0]

            data_type[columnName] = max_value

        print(data_type)

        #Changing the datatype

        change = []

        for (columnName, columnData) in data.iteritems():

            if data_type[columnName] ==  'DateTime':

                data_type_before = str(detect_series_type(data[columnName],typeset))

                data[columnName] = pd.to_datetime(data[columnName], errors = 'coerce')

                if data_type_before != str(detect_series_type(data[columnName],typeset)):

                    print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_series_type(data[columnName],typeset)))


            elif (data_type[columnName] ==  'Integer') or (data_type[columnName] ==  'Float'):

                data_type_before = str(detect_series_type(data[columnName],typeset))

                data[columnName] = pd.to_numeric(data[columnName], errors = 'coerce')

                if data_type_before != str(detect_series_type(data[columnName],typeset)):

                    print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_series_type(data[columnName],typeset)))

                
            elif data_type[columnName] ==  'TimeDelta':

                data_type_before = str(detect_series_type(data[columnName],typeset))

                data[columnName] = pd.to_timedelta(data[columnName], errors = 'coerce')

                if data_type_before != str(detect_series_type(data[columnName],typeset)):

                    print(columnName, " column data was changed from ", data_type_before , " to ", str(detect_series_type(data[columnName],typeset)))

            else:

                data[columnName] = data[columnName]

    
        #Finding the number of missing data
        before = data.shape[0]
        data_copy = data.copy()
        data_copy.dropna(inplace = True)
        after = data_copy.shape[0]
        null_data = before - after

        print("There are altogether ", null_data, "in the dataset.")

        #options for handling missing data

        print("Enter 1 if you want to drop all the rows with missing value")
        print("Enter 2 if you want to fill the missing values of numerical type columns with 0")
        print("Enter 3 if you want to fill the missing values of numerical type columns with median")
        print("Enter 4 if you want to leave the data as it is")


        #Getting the user input
        while True:
            try:
                x=int(input("Your Selection: "))
                if x in [1,2,3,4]:
                    break
                else:
                    print("The option is not available. Please try again")
            except:
                print("Invalid selection. Please try again")


        #Handling the missing data according to the selection
        if x == 1:
            #dropping all the rows with missing value
            data = data.dropna()
        elif x == 2:
            #Iterating through each column
            for (colName,colValue) in data.iteritems():
                #Filling the missing value with 0 for only numerical columns
                type_of_column = str(detect_series_type(data[colName],typeset))
                if (type_of_column == "Integer") or (type_of_column == "Float"):
                    data[colName] = data[colName].fillna(0)
        elif x == 3:
            for (colName,colValue) in data.iteritems():
                #Filling the missing value with median for only numerical columns
                type_of_column = str(detect_series_type(data[colName],typeset))
                if (type_of_column == "Integer") or (type_of_column == "Float"):
                    med = data[colName].median()
                    data[colName] = data[colName].fillna(med)
        else:
            data = data


        after_final = data.shape[0]

        dropped_rows = before - after_final

        print(dropped_rows, " rows were dropped.")

        #Checking Duplicate

        before = data.shape[0] 
        bool_series = data.duplicated(keep = False) 
            
        # bool series 
        bool_series 
            
        # passing NOT of bool series to see unique values only 
        data = data[~bool_series] 
        after = data.shape[0]

        data_drop = before - after

    return data        
