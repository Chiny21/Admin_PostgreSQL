import psycopg2
import sys
import getpass
import os
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("Chiny DB-A")

databaseConnection = None
theCursor = None

def connectToDatabase():
    global databaseConnection
    global theCursor
    try:
        print("Please, type the following information to connect to the database.")
        host = input("Host: ")
        database = input("Database: ")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        databaseConnection = psycopg2.connect(dbname=database, user=username, password=password,
                                          host=host, port="5432")
        theCursor = databaseConnection.cursor()
        os.system('cls')
        print("Welcome!")
        chooseFromMainMenu()
    except psycopg2.OperationalError as theError:
        print("Something went wrong connecting to the dabase. Make sure the information you entered is correct. "
              "Please, try again. \n" + str(theError))
        connectToDatabase()


def checkToQuit(theInput):
    if theInput == "/quit":
        theCursor.close()
        sys.exit()

def createTableFromMenu():
    try:
        tableName = input("Type the following information for this statement. \nTable Name: ")
        theStatement = "CREATE TABLE " + tableName + "("
        columnNumber = input("How many columns will " + tableName + " have?")
        columnNumberToNumber = int(columnNumber)
        print("Type the corresponding information for each column.")

        for eachColumn in range (0, columnNumberToNumber):
            theAttribute = input("Attribute: ").strip()
            theStatement = theStatement + theAttribute + " "
            dataType = input("Data Type: ").strip()
            theStatement = theStatement + dataType + " "
            columnConstraint = input("Column Constraint: ").strip()
            theStatement = theStatement + columnConstraint + ","
            print("\nNext Column:")

        theStatement = theStatement[:-1] + ");"
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table created.")
        chooseFromCreateMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + theError)
        createTableFromMenu()

def createFunctionFromMenu():
    try:
        thePath = input("Type the following information for this statement. \nFunction File Path: ")
        theFile = open(thePath)
        theStatement = theFile.read()
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function created.")
        chooseFromCreateMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + theError)
        chooseFromCreateMenu()

def createIndexFromMenu():
    try:
        IndexName = input("Type the following information for this statement. \nIndex Name: ")
        TableName = input("Table Name: ")
        ColumnName = input("Column Name: ")
        theStatement = "CREATE UNIQUE INDEX %s ON %s (%s);" % (IndexName, TableName, ColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index created.")
        chooseFromCreateMenu
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + theError)
        chooseFromCreateMenu()

theCreateMenu = "\nType /back to return to the previous menu. \nCreate Menu: \n1. TABLE \n2. FUNCTION " \
                    "\n3. INDEX \nChoose an option: "

def chooseFromCreateMenu():
    try:
        theInput = input(theCreateMenu)
        if theInput == "/back":
            chooseFromDDLMenu()
        else:
            return {
                '1': createTableFromMenu,
                '2': createFunctionFromMenu,
                '3': createIndexFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + theError)
        chooseFromDDLMenu()

def addColumnFromMenu():
    try:
        TableName = input("Type the following information for this statement. \nTable Name:")
        ColumnName = input("Column Name: ")
        DataType = input("Data Type: ")
        theStatement = "ALTER TABLE %s ADD %s %s;"%(TableName,ColumnName,DataType)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column added.")
        alterTableFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + theError)
        alterTableFromMenu()

def removeColumnFromMenu():
    try:
        TableName = input("Type the following information for this statement. \nTable Name:")
        ColumnName = input("Column Name: ")
        theStatement = "ALTER TABLE %s DROP %s CASCADE;"%(TableName,ColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column removed.")
        alterTableFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + theError)
        alterTableFromMenu()

def renameColumnFromMenu():
    try:
        TableName = input("Type the following information for this statement. \nTable Name:")
        ColumnName = input("Column Name: ")
        newColumnName = input("New Column Name: ")
        theStatement = "ALTER TABLE %s RENAME %s TO %s;"%(TableName,ColumnName,newColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column renamed.")
        alterTableFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        alterTableFromMenu()

def renameTableFromMenu():
    try:
        TableName = input("Type the following information for this statement. \nTable Name:")
        NewTableName = input("New Table Name: ")
        theStatement = "ALTER TABLE %s RENAME TO %s;"%(TableName,NewTableName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table renamed.")
        alterTableFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        alterTableFromMenu()

def alterTableFromMenu():
    try:
        theInput = input("\nType /back to return to the previous menu. \nAlter Table Menu: \n1. Add Column \n2. Remove Column " \
                    "\n3. Rename Column \n4. Rename Table \nChoose an option: ")
        if theInput == "/back":
            chooseFromAlterMenu()
        else:
            return {
                '1': addColumnFromMenu,
                '2': removeColumnFromMenu,
                '3': renameColumnFromMenu,
                '4': renameTableFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + str(theError))
        chooseFromDDLMenu()

def RenameFunctionFromMenu():
    try:
        FunctionName = input("Type the following information for this statement. Please, separate multiple values"
                             "with a comma. \nFunction Name: ")
        ParameterType = input("Parameter Types: ")
        FormattedParameterType = ParameterType.replace(' ','')
        NewFunctionName = input("New Function Name: ")
        theStatement = "ALTER FUNCTION %s(%s) RENAME TO %s;"%(FunctionName, FormattedParameterType, NewFunctionName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function renamed.")
        chooseFromAlterMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromAlterMenu()

def RenameIndexFromMenu():
    try:
        IndexName = input("Type the following information for this statement. \nIndex Name: ")
        NewIndexName = input("\nNew Index Name: ")
        theStatement = "ALTER INDEX %s RENAME TO %s;"%(IndexName,NewIndexName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index renamed.")
        chooseFromAlterMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromAlterMenu()

def chooseFromAlterMenu():
    try:
        theInput = input(theCreateMenu)
        if theInput == "/back":
            chooseFromDDLMenu()
        else:
            return {
                '1': alterTableFromMenu,
                '2': RenameFunctionFromMenu,
                '3': RenameIndexFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + str(theError))
        chooseFromDDLMenu()

def dropTableFromMenu():
    try:
        TableNames = input("Type the following information for this statement. Please, separate the values with a comma. "
                           "\nTable Name(s):")
        FormattedTableNames = TableNames.replace(' ','')
        theStatement = "DROP TABLE %s CASCADE;"%(FormattedTableNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table dropped.")
        chooseFromDropMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromDropMenu()

def dropFunctionFromMenu():
    try:
        FunctionName = input("Type the following information for this statement. Please, separate multiple values with a comma. "
                           "\nFunction Name: ")
        ParameterType = input("Parameter Types: ")
        FormattedParameterTypes = ParameterType.replace(' ', '')
        theStatement = "DROP FUNCTION %s(%s);" % (FunctionName, FormattedParameterTypes)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function dropped.")
        chooseFromDropMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromDropMenu()

def dropIndexFromMenu():
    try:
        IndexNames =input("Type the following information for this statement. Please, separate the values with a comma. "
                           "\nIndex Name(s):")
        FormattedIndexNames = IndexNames.replace(' ','')
        theStatement = "DROP INDEX %s CASCADE;"%(FormattedIndexNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index dropped.")
        chooseFromDropMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromDropMenu()

def chooseFromDropMenu():
    try:
        theInput = input(theCreateMenu)
        if theInput == "/back":
            chooseFromDDLMenu()
        else:
            return {
                '1': dropTableFromMenu,
                '2': dropFunctionFromMenu,
                '3': dropIndexFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + str(theError))
        chooseFromDDLMenu()

def truncateTableFromMenu():
    try:
        TableNames = input("Type the following information for this statement. Please, separate the values with a comma. "
            "\nTable Name(s):")
        FormattedTableNames = TableNames.replace(' ','')
        theStatement = "TRUNCATE %s CASCADE;"%(FormattedTableNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table truncated.")
        chooseFromDDLMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        chooseFromDDLMenu()

theDDLMenu = "\nType /back to return to the previous menu. \nDDL Menu: \n1. CREATE \n2. ALTER \n3. DROP " \
             "\n4. TRUNCATE \nChoose an option: "

def chooseFromDDLMenu():
    try:
        theInput = input(theDDLMenu)
        if theInput == "/back":
            chooseFromMainMenu()
        else:
            return {
                '1': chooseFromCreateMenu,
                '2': chooseFromAlterMenu,
                '3': chooseFromDropMenu,
                '4': truncateTableFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + str(theError))
        chooseFromDDLMenu()

def showTableColumns(TableName):
    try:
        theInput = input("Do you want to see the table's columns? \n1. Yes \n2. No \nChoose an option: ").strip()
        if theInput == "1":
            theQuery = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '" + TableName + "';"
            theCursor.execute(theQuery)
            for eachRow in theCursor:
                print("Column Name: " + eachRow[0] + " | Data Type: " + eachRow[1])
        elif theInput != "2":
            raise KeyError
    except KeyError:
        print("\nError: invalid option. Please, try again.")
        showTableColumns(TableName)

def selectFromMenu():
    try:
        tableName = input("Type the following information for this statement. \nTable Name:")
        theStatement = "SELECT "
        seeTable = input("Do you want to see the table's columns? \n1. Yes \n2. No \nChoose an option: ").strip()
        if seeTable == "1":
            theQuery = "SELECT column_name FROM information_schema.columns WHERE table_name = '" + tableName + "';"
            theCursor.execute(theQuery)
            theColumns = "Columns: "
            for eachRow in theCursor:
                theColumns = theColumns + eachRow[0] + ", "
            print(theColumns[:-2])
        elif seeTable != "2":
            raise KeyError
        theSelectedColumns = input("Type the columns to select and separate them by a comma. \nColumns: ").strip()
        theSelectedColumnsList = [x.strip() for x in theSelectedColumns.split(',')]
        for eachValue in theSelectedColumnsList:
            theStatement = theStatement + eachValue + ","
        theStatement = theStatement[:-1] + " FROM " + tableName
        includeWhereClause = input("Do you want to add a WHERE clause? \n1. Yes \n2. No \nChoose an option: ").strip()
        if includeWhereClause == "1":
            theStatement = theStatement + " WHERE "
            theWhereClauseColumn = input("Column: ")
            theStatement = theStatement + theWhereClauseColumn + " = "
            theWhereClauseValue = input("Value: ")
            theStatement = theStatement + theWhereClauseValue
        elif includeWhereClause != "2":
            raise KeyError
        theStatement = theStatement + ";"
        theCursor.execute(theStatement)
        for eachRow in theCursor:
            theRow = ""
            for eachValue in eachRow:
                theRow = theRow + str(eachValue) + " | "
            print(theRow)
        chooseFromDMLMenu()
    except KeyError:
        print("Error: Invalid option selected. Please, start again.")
        selectFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: Invalid data entered. Please, try again. \n" + str(theError))
        selectFromMenu()

def insertFromMenu():
    try:
        tableName = input("Type the following information for this statement. \nTable Name:")
        theStatement = "INSERT INTO " + tableName + " VALUES ("
        seeTable = input("Do you want to see the table's columns? \n1. Yes \n2. No \nChoose an option: ").strip()
        if seeTable == "1":
            theQuery = "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '" + tableName + "';"
            theCursor.execute(theQuery)
            for eachRow in theCursor:
                print("Column: " + eachRow[0] + " | Data Type: " + eachRow[1])
        elif seeTable != "2":
            raise KeyError
        theValues = input("Type the values in the corresponding column order and separated by a comma. Please, type the"
                          "non-numeric values between single quotes. \nValues: ").strip()
        theValuesList = [x.strip() for x in theValues.split(',')]
        for eachValue in theValuesList:
            theStatement = theStatement + eachValue + ","
        theStatement = theStatement[:-1] + ");"
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values inserted.")
        chooseFromDMLMenu()
    except KeyError:
        print("Error: Invalid option selected. Please, start again.")
        insertFromMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: Invalid data entered. Please, try again. \n" + str(theError))
        insertFromMenu()

def updateFromMenu():
    try:
        tableName = input("\nType the following information for this statement. \nTable Name: ").strip()
        showTableColumns(tableName)
        columnName = input("\nColumn to Change: ").strip()
        newValue = input("\nNew Value: ").strip()
        referenceColumn = input("\nReference Column: ").strip()
        oldValue = input("\nOld Value:").strip()
        theStatement = "UPDATE %s SET %s = %s WHERE %s = %s;"%(tableName,columnName,newValue,referenceColumn,oldValue)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values updated.")
        chooseFromDMLMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        updateFromMenu()

def deleteFromMenu():
    try:
        tableName = input("\nType the following information for this statement. \nTable Name: ").strip()
        showTableColumns(tableName)
        columnName = input("Reference Column: ").strip()
        columnValue = input("Value: ").strip()
        theStatement = "DELETE FROM %s WHERE %s = %s;" % (tableName, columnName, columnValue)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values deleted.")
        chooseFromDMLMenu()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        deleteFromMenu()

theDMLMenu = "\nType /back to return to the previous menu. \nDML Menu: \n1. SELECT \n2. INSERT \n3. UPDATE " \
             "\n4. DELETE \nChoose an option: "

def chooseFromDMLMenu():
    try:
        theInput = input(theDMLMenu)
        if theInput == "/back":
            chooseFromMainMenu()
        else:
            return {
                '1': selectFromMenu,
                '2': insertFromMenu,
                '3': updateFromMenu,
                '4': deleteFromMenu
            }[theInput]()
    except KeyError as theError:
        print("\nError: invalid option. Please, try again. \n" + str(theError))
        chooseFromDMLMenu()

availableCommands = {"CreateTable {Name, Attributes, DataTypes, Constraints}",
                    "Update {TableName, ColumnName, NewValue, ReferenceColumn, OldValue}",
                    "Select {Columns,Table,WhereColumn,Value}",
                    "Insert {TableName, Values}",
                    "Delete {TableName, ColumnName, Value",
                     "AddColumn {TableName, ColumnName, DataType}",
                     "RemoveColumn {TableName, ColumnName}",
                     "RenameColumn {TableName, ColumnName, NewColumnName}",
                     "RenameTable {TableName, NewTableName}",
                     "DropTable {TableNames}",
                     "TruncateTable {TableNames}",
                     "CreateIndex {IndexName, TableName, ColumnName}", "DropIndex {IndexNames}",
                     "RenameIndex {IndexName, NewIndexName}",
                     "CreateFunction {Path}", "RenameFunction {FunctionName, ParameterType, NewFunctionName}",
                     "DropFunction {FunctionName, ParameterTypes}"}

def showFunctions():
    functionNumber = 1
    for eachElement in availableCommands:
        print(str(functionNumber) + ". " + eachElement)
        functionNumber += 1

def CreateTable(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        Name = theParameterList[0]
        theColumns = ''
        for eachColumn in theParameterList[1:]:
            FormattedColumn = eachColumn.replace('-',' ')
            theColumns += FormattedColumn + ','
        theColumns = theColumns[:-1]
        theStatement = "CREATE TABLE %s (%s);"%(Name,theColumns)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table created.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def AddColumn(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        ColumnName = theParameterList[1]
        DataType = theParameterList[2]
        theStatement = "ALTER TABLE %s ADD %s %s;"%(TableName,ColumnName,DataType)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column added.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def RemoveColumn(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        ColumnName = theParameterList[1]
        theStatement = "ALTER TABLE %s DROP %s CASCADE;"%(TableName,ColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column removed.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def RenameColumn(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        ColumnName = theParameterList[1]
        newColumnName = theParameterList[2]
        theStatement = "ALTER TABLE %s RENAME %s TO %s;"%(TableName,ColumnName,newColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Column renamed.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def RenameTable(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        NewTableName = theParameterList[1]
        theStatement = "ALTER TABLE %s RENAME TO %s;"%(TableName,NewTableName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table renamed.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def DropTable(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        if len(theParameterList) > 1:
            raise IndexError
        TableNames = theParameterList[0]
        FormattedTableNames = TableNames.replace('-',',')
        theStatement = "DROP TABLE %s CASCADE;"%(FormattedTableNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table dropped.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def TruncateTable(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        if len(theParameterList) > 1:
            raise IndexError
        TableNames = theParameterList[0]
        FormattedTableNames = TableNames.replace('-',',')
        theStatement = "TRUNCATE %s CASCADE;"%(FormattedTableNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Table truncated.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def CreateFunction(Path):
    try:
        theFile = open(Path)
        theStatement = theFile.read()
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function created.")
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def RenameFunction(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        FunctionName = theParameterList[0]
        ParameterType = theParameterList[1]
        FormattedParameterType = ParameterType.replace('-',',')
        NewFunctionName = theParameterList[2]
        theStatement = "ALTER FUNCTION %s(%s) RENAME TO %s;"%(FunctionName, FormattedParameterType, NewFunctionName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function renamed.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def DropFunction(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        FunctionName = theParameterList[0]
        ParameterType = theParameterList[1]
        FormattedParameterTypes = ParameterType.replace('-',',')
        theStatement = "DROP FUNCTION %s(%s);"%(FunctionName,FormattedParameterTypes)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Function dropped.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def CreateIndex(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        IndexName = theParameterList[0]
        TableName = theParameterList[1]
        ColumnName = theParameterList[2]
        theStatement = "CREATE UNIQUE INDEX %s ON %s (%s);" % (IndexName, TableName, ColumnName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index created.")
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def RenameIndex(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        IndexName = theParameterList[0]
        NewIndexName = theParameterList[1]
        theStatement = "ALTER INDEX %s RENAME TO %s;"%(IndexName,NewIndexName)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index renamed.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def DropIndex(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        if len(theParameterList) > 1:
            raise IndexError
        IndexNames = theParameterList[0]
        FormattedIndexNames = IndexNames.replace('-',',')
        theStatement = "DROP INDEX %s CASCADE;"%(FormattedIndexNames)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Index dropped.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def Select(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        Columns = theParameterList[0]
        FormattedColumns = Columns.replace(' ','').replace('-',',')
        TableName = theParameterList[1]
        if len(theParameterList) == 2:
            theStatement = "SELECT %s FROM %s;" % (FormattedColumns, TableName)
        elif len(theParameterList) == 4:
            ReferenceColumn = theParameterList[2]
            Value = theParameterList[3]
            theStatement = "SELECT %s FROM %s WHERE %s = %s;"%(FormattedColumns,TableName,ReferenceColumn,Value)
        theCursor.execute(theStatement)
        for eachRow in theCursor:
            theRow = ""
            for eachValue in eachRow:
                theRow = theRow + str(eachValue) + " | "
            print(theRow)
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def Insert(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        Values = theParameterList[1]
        FormattedValues = Values.replace(' ', '').replace('-', ',')
        theStatement = "INSERT INTO %s VALUES(%s);"%(TableName,FormattedValues)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values inserted.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def Update(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        ColumnName = theParameterList[1]
        NewValue = theParameterList[2]
        ReferenceColumn = theParameterList[3]
        OldValue = theParameterList[4]
        theStatement = "UPDATE " + TableName + " SET " + ColumnName + " = " + NewValue + " WHERE " + ReferenceColumn + " = " + OldValue + ";"
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values updated.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

def Delete(Parameters):
    try:
        theParameterList = [x.strip() for x in Parameters.split(',')]
        TableName = theParameterList[0]
        ColumnName = theParameterList[1]
        Value = theParameterList[2]
        theStatement = "DELETE FROM %s WHERE %s = %s;"%(TableName,ColumnName,Value)
        theCursor.execute(theStatement)
        databaseConnection.commit()
        print("Success! Values deleted.")
        typeCommand()
    except IndexError as theError:
        print("Error: invalid amount of parameters. Please, try again. \n" + str(theError))
        typeCommand()
    except psycopg2.DatabaseError as theError:
        print("\nError: invalid data entered. Please, try again. \n" + str(theError))
        typeCommand()

fuctionDict = {'CreateTable':CreateTable, 'Update':Update, 'Select':Select, 'Insert':Insert, 'Delete':Delete,
               'AddColumn':AddColumn, 'RemoveColumn':RemoveColumn, 'RenameColumn':RenameColumn,
               'RenameTable':RenameTable, 'DropTable':DropTable, 'TruncateTable':TruncateTable,
               'CreateIndex':CreateIndex, 'DropIndex':DropIndex, 'RenameIndex':RenameIndex,
               'CreateFunction':CreateFunction, 'RenameFunction':RenameFunction, 'DropFunction':DropFunction}

def typeCommand():
        while True:
            theStatement = input("\nType /quit to close the Database Administrator. "
                                 "\nType /help to see all available functions. "
                                 "\nWarning: Separate parameters with a comma and multiple parameter values with a dash."
                                 "\nCommand:")
            checkToQuit(theStatement)
            if theStatement == "/help":
                showFunctions()
            else:
                theFunction = theStatement.partition("{")[0].strip()
                theParameters = theStatement.partition('{')[2][:-1]
                fuctionDict[theFunction](theParameters)

theMainMenu = "\nType /quit to close Chiny DB-A. \nMain Menu: \n1. DDL \n2. DML \n3. CMD" \
              "\nChoose an option: "

def chooseFromMainMenu():
        try:
            theInput = input(theMainMenu)
            checkToQuit(theInput)
            return {
                '1': chooseFromDDLMenu,
                '2': chooseFromDMLMenu,
                '3': typeCommand
            }[theInput]()
        except KeyError as theError:
            print("\nError: invalid option. Please, try again. \n" + str(theError))
            chooseFromMainMenu()

connectToDatabase()