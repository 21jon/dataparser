

import os
import sqlite3
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_database_connection(database_name):
    engine = sqlite3.connect(database_name)
    return engine


def data_import_csv(data_set_path):
    df = pd.read_csv(data_set_path, parse_dates=[
                     'time']).sort_values(by='time')
    return df


def data_to_sql(data_frame: pd.DataFrame, table_name, engine, ):
    data_frame.to_sql(table_name, con=engine,
                      if_exists='replace', index=False, )


def data_to_plot(data_frame: pd.DataFrame, plot_path):
    min = data_frame.iloc[0]['time']
    max = data_frame.iloc[-1]['time']

    span = max - min
    span = span.total_seconds() * 100
    temp = round((span / len(data_frame.index)), 0)

    x_values = np.arange(start=0, stop=len(
        data_frame.index), step=temp).tolist()

    plt.plot(x_values, data_frame['bar'].tolist())
    plt.legend(['bar'])

    plt.savefig(plot_path, dpi=1200,)


def find_extreme_values(data_frame: pd.DataFrame, column_name):
    max_value = data_frame[column_name].max()
    min_value = data_frame[column_name].min()
    return max_value, min_value


def userinput():
    data_set_path = None
    try:
        data_set_path = os.path.abspath(sys.argv[1])
    except IndexError:
        print("Please provide a path to the data set")
        sys.exit(1)

    tabelName = input("Enter the name of the table: ")
    if not tabelName:
        tabelName = "data"

    picturename = input("Enter the name of the picture: ")
    if not picturename:
        picturename = "plot"

    database_name = os.path.abspath("./results/data.db")
    plot_set_path = os.path.abspath(f"./results/{picturename}.png")

    print(f"Data set path: {data_set_path}")
    print(f"Database name: {database_name}")
    print(f"Plot path: {plot_set_path}")
    print(f"Table name: {tabelName}")

    if input("Continue? (y/n): ") == "n":
        exit(code=0)

    return data_set_path, tabelName, database_name, plot_set_path


def main():
    # Set the path to the data set and database
    data_set_path, tabelName, database_name, plot_set_path = userinput()
    # User information about the data set

    # Create a database connection and import the dataset into the database
    engine = create_database_connection(database_name)
    print("Database connection created")
    data_frame = data_import_csv(data_set_path)
    print("Data imported")
    data_to_sql(data_frame, tabelName, engine)
    print("Data imported to database")
    engine.close()
    print("Database connection closed")
    # Create a plot of the data set
    print("Creating plot")
    data_to_plot(data_frame, plot_set_path)
    print("Plot created")

    print("Done")


if __name__ == "__main__":
    main()
