import copy
import sqlite3
import pandas as pd
import os
import argparse

def combine_sqlite_dbs(directory: str, database_name: str = "stream_data.db") -> pd.DataFrame:
    features = ["index_n", "frames_received_count", "frames_dropped", "calculcated_fps", "calculated_latency"]
    params = ["image_size", "fps", "cpu", "memory", "task_id"]
    features_and_params = copy.copy(features)
    features_and_params.extend(params)
    result_dataframe = pd.DataFrame(columns=features_and_params)
    sql_query = "select minute_count, frames_received, frames_dropped, avg_calculated_fps, avg_calculated_latency from stream_data_final;"
    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)
        if not os.path.isdir(full_path):
            continue
        params = file_name.split("-")
        if not len(params) == 5:
            print(f"skipping {file_name} because it doesn't fit the schema 'image_size-fps-cpu-memory-task_id")
            continue
        params_dict = {"image_size": params[0], "fps": params[1], "cpu": params[2], "memory":params[3], "task_id":params[4]}
        if database_name not in os.listdir(full_path):
            print(f"{database_name} not found in {full_path}, continuing")
            continue
        database_path = os.path.join(full_path, database_name)
        db_connection = sqlite3.connect(database_path)
        cursor = db_connection.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        new_dataframe = pd.DataFrame(results, columns=features)
        new_dataframe.reset_index(inplace=True, drop=True)
        for param_name, param_value in params_dict.items():
            new_dataframe[param_name] = param_value
        cols_1 = list(result_dataframe.columns)
        cols_2 = list(new_dataframe.columns)
        result_dataframe = pd.concat([result_dataframe, new_dataframe])
        db_connection.close()
    result_dataframe = result_dataframe.drop(["frames_received_count"], axis=1)
    return result_dataframe

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=None, required=True, help="Provide a directory with stream results in them")
    parser.add_argument("-o", "--outfile", default="final_data.csv", help="Name for genenerated CSV file")
    return parser

def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    result: pd.Dataframe = combine_sqlite_dbs(args.directory)
    result.to_csv(args.outfile)

if __name__ == '__main__':
    main()