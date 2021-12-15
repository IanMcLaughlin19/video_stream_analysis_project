import sqlite3
import pandas as pd
import os

def combine_sqlite_dbs(directory: str, database_name: str = "stream_data.db") -> pd.DataFrame:
    columns = ["index", "minute_count", "fps", "frames_received_count", "frames_dropped", "calculcated_fps", "calculated_latency"]
    params = ["analysis_number", "image_size", "fps", "memory", "task_id"]
    result_dataframe = pd.DataFrame(columns=columns)
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if not os.path.isdir(full_path):
            continue
        params = file_name.split("-")
        if not len(params) == 5:
            continue
        image_size, fps, cpu, memory, task_id = params[0], params[1], params[2], params[3], params[4]
        if database_name not in os.listdir(full_path):
            print(f"{database_name} not found in {full_path}, continuing")
            continue
        database_path = os.path.join(full_path, database_name)
        db_connection = sqlite3.connect(database_path)
        cursor = db_connection.cursor()
        sql_query = "select * from stream_data_final;"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        new_dataframe = pd.DataFrame(results, columns=columns)
        result_dataframe = pd.concat([result_dataframe, new_dataframe])
        db_connection.close()
    return new_dataframe

if __name__ == '__main__':
    path = "C:\\Users\\ianm1\\PycharmProjects\\video_stream_analysis_project\\scripts"
    test_combined = combine_sqlite_dbs(path)
    print("test!")