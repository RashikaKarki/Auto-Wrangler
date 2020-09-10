from visions.functional import cast_to_inferred, detect_type, infer_type
from visions.typesets import StandardSet


from clean_module import *



typeset = StandardSet()



def Main_func(data):
    flag = 0
    #Handling Datatype
    if flag == 0:
        #Finding datatype
        data_type = Datatype(data)
        #Changing Datatype
        data = changedt(data, data_type)
        #Finding the number of missing data
        null_data,before = findnull(data)
        print("There are altogether ", null_data, "null in the dataset.")
        percent_missing = data.isnull().sum() * 100 / len(data)
        for (colName,colValue) in data.iteritems():
          if percent_missing[colName] >= 40:
              data = data.drop([colName], axis=1)
              print(colName, " column was dropped.")  
        for (colName,colValue) in data.iteritems():
          #Filling the missing value with median for only numerical columns
          type_of_column = str(detect_type(data[colName],typeset))
          if (type_of_column == "Integer") or (type_of_column == "Float"):
            med = data[colName].median()
            data[colName] = data[colName].fillna(med)
        data = data.dropna()
        after = data.shape[0]
        dropped_rows = before - after
        print(dropped_rows, " rows were dropped.")
        #Checking Duplicate
        before = data.shape[0] 
        bool_series = data.duplicated(keep = False)           
        # passing NOT of bool series to see unique values only 
        data = data[~bool_series] 
        after = data.shape[0]
        data_drop = before - after
    return data