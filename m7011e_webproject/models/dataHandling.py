#Upload data to the database
def uploadFile(file):
    #Get the file extension
    file_extension = file.filename.split('.')[-1]
    #Check if the file is a csv file
    if file_extension == 'csv':
        #Read the file
        data = pd.read_csv(file)
        #Get the column names
        columns = data.columns
        #Get the table name
        table_name = file.filename.split('.')[0]
        #Create the table
        createTable(table_name, columns)
        #Insert the data
        insertData(table_name, data)
        return True
    else:
        return False