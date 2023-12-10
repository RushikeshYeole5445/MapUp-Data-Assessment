"""
Question 1: Car Matrix Generation
Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
values from id_2 as columns
values from id_1 as index
dataframe should have values from car column
diagonal values should be 0.
"""

import pandas as pd
import numpy as np

def generate_car_matrix(df):
    # Load the dataset into a DataFrame

    # Create a pivot table using id_1 as index, id_2 as columns, and car as values
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set diagonal values to 0
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix



"""Question 2: Car Type Count Calculation
Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
low for values less than or equal to 15,
medium for values greater than 15 and less than or equal to 25,
high for values greater than 25.
Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.
"""

import pandas as pd
import numpy as np

def get_type_count(df):
    # Add a new categorical column 'car_type' based on values of the 'car' column
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    choices = ['low', 'medium', 'high']
    df['car_type'] = pd.Series(np.select(conditions, choices, default=np.nan), dtype="category")

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))
    return type_counts


"""Question 3: Bus Count Index Retrieval
Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.
"""




def get_bus_indexes(df)->list:
    ind_list = df[df["bus"]> 2*(df["bus"].mean())].index.to_list()
    return ind_list

"""Question 4: Route Filtering
Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.
"""


def filter_routes(df):
    avg_truck_per_route = df.groupby('route')['truck'].mean()
    selected_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()
    selected_routes.sort()

    return selected_routes



def multiply_matrix(matrix):
    for i in matrix.index:
        for j in matrix.columns:
            if matrix[i][j]>20:
                matrix[i][j] = matrix[i][j]*0.75
            else:
                matrix[i][j] = matrix[i][j]*1.25

    return matrix



def check_time_completeness(df):
    # Combine 'startDay' and 'startTime' columns to create a new 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')

    # Combine 'endDay' and 'endTime' columns to create a new 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    completeness_check = (
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.time != pd.Timestamp('00:00:00').time()) |
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.time != pd.Timestamp('23:59:59').time()) |
        (df.groupby(['id', 'id_2'])['start_timestamp'].min().dt.dayofweek != 0) |  
        (df.groupby(['id', 'id_2'])['end_timestamp'].max().dt.dayofweek != 6))


    return completeness_check
