import dataManagement as db
import pandas as pd

dataMgr = db.dataManagement()

dataTasks = pd.read_csv('task_data.csv')

for index, row in dataTasks.iterrows():
    id = row['id']
    timestamp = row['timestamp']
    temperature = row['temperature']
    duration = row['duration']

    comitted = dataMgr.insertToData(id, timestamp, temperature, duration)
    if comitted == False:
        print("Error storing id: ", str(id))