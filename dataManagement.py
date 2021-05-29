import sqlite3 as db
import pandas as pd

class dataManagement:

    def __init__(self, databaseName = 'process_data.db'):
        self.database = databaseName
        self.Tables = ['data', 'log']
        self.checkTablesExists()

    def insertToData(self, id, timestamp, temperature, duration):
        try:
            sqlQuery = "INSERT INTO data (id,timestamp,temperature,duration) VALUES (?,?,?,?)"
            returnInfo = self.executeQuery(sqlQuery,[id, timestamp, temperature, duration])
            return returnInfo
        except:
            return False

    def logRecord(self,timestamp, idrequested):
        try:
            sqlQuery = "INSERT INTO log (timestamp,idrequested) VALUES (?,?)"
            returnInfo = self.executeQuery(sqlQuery,[timestamp, idrequested])
            return returnInfo
        except:
            return False


    def getDataFromTable(self, id = 0):
        sqlQuery = "SELECT * FROM data "
        if id > 0:
            sqlQuery += " WHERE id = ?"
            sqlRequest = self.dataQuery(sqlQuery,[id])
            return sqlRequest
        else:
            sqlRequest = self.dataQuery(sqlQuery)
            return sqlRequest

    def checkTablesExists(self):
            for table in self.Tables:
                query = "SELECT name FROM sqlite_master WHERE type='table' and name='{}';".format(table)
                tableReturn = self.dataQuery(query)
                if len(tableReturn) == 0: self.executeQuery(self.createSchema(table))

        
    def executeQuery(self, query, values = None):
        try:
            conn = db.connect(self.database)
            cursor = conn.cursor()
            if values == None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)

            conn.commit()
            conn.close()
            return True
        except:
            return False

    def dataQuery(self, query, values = None):
            conn = db.connect(self.database)
            cursor = conn.cursor()

            if values == None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)

            cols = [column[0] for column in cursor.description]
            queryData = cursor.fetchall()

            returnData = pd.DataFrame.from_records(data = queryData, columns = cols)

            conn.close()
            return returnData

    def createSchema(self, table):
        sql = ''
        if table == 'data':
            sql += ' CREATE TABLE data ('
            sql += '         id          INTEGER  PRIMARY KEY AUTOINCREMENT,'
            sql += '         timestamp   DATETIME,'
            sql += '         temperature DOUBLE,'
            sql += '         duration    VARCHAR'
            sql += '     )'
            return sql

        if table == 'log':
            sql = ''
            sql += ' CREATE TABLE log ('
            sql += '         id          INTEGER  PRIMARY KEY AUTOINCREMENT,'
            sql += '         timestamp   DATETIME,'
            sql += '         idrequested    VARCHAR'
            sql += '     )'
            return sql
