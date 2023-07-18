#Task 1 ,Dhruv Talan
# defining the function we will need to convert our date into the following fromat of dd-mm-yyy
from datetime import datetime


def convert_suitably(data_str):
    date_obj = datetime.strptime(data_str, "%d/%m/%Y")
    new_date_str = date_obj.strftime("%d-%m-%Y")
    return new_date_str


import requests
from bs4 import BeautifulSoup
import pandas as pd

# import all the necessary libraies

data_final_list = []
for year in range(2008, 2024):
    # used an fstring here to get the urls of all the years iteratively

    URL = f'https://www.teaboard.gov.in/WEEKLYPRICES/{year}'
    response = requests.get(URL)
    Soup = BeautifulSoup(response.content, 'html.parser')
    tables = Soup.find_all('table')
    second_table = tables[1]

    # I obsereved that second table is the table whose data needs to be collected

    tr_first = second_table.find('tr')
    th = tr_first.find_all('b')
    c_n = []
    for col_name in th:
        c_n.append(col_name.text)

    '''
    Getting the header names of the table using the first <tr> element and the header cells in it 
    '''
    lencn = len(c_n)  # reprents the totaL no of cells in the header row
    # print(lencn)

    # removed the weekly day time , simply dont need it and created
    tr_all = second_table.find_all('tr')
    relevant_tr = tr_all[1:]

    cell = []
    for tr in relevant_tr:
        for row in tr.find_all('td'):
            for data in row.find_all('span'):
                cell.append(data.text)
    lencell = len(cell)  # represnts total no of cells in the table
    # print(lencell)
    a = int(lencell / lencn)
    # print(a)  # a means basically the number of rows

    c_n.pop(lencn - 1)  # we dont want the first and last elemnt that's why popping them out
    c_n.pop(0)
    c_n = [c_n[i] for j in range(0, a) for i in
           range(0, lencn - 2)]  # creating the location list which is just a repetition of locations
    # lencn-2 becuase we dont need the first and the last column i.e weekly/date time and tea serve columns repectively

    nested_list = []
    for i in range(0, lencell, lencn):
        nested_list.append(
            cell[i:i + lencn])  # making my nested list such that it contanis rows as elemnts of the table

    for lict in nested_list:
        lict = lict.pop(lencn - 1)  # popping the unwanted tea serve column value

    day = []
    average_prices = []
    for lict in nested_list:
        day.append(lict[0])
        average_prices.append(lict[1:])
    list_of_entries = []
    week_date = []
    df = pd.DataFrame({'Week': week_date,
                       'average_price': list_of_entries})  # creating my dataframe for a particular value of date just an example

    df_list = []

    for i, j in zip(day, average_prices):
        week_date = [i] * 8
        df = pd.DataFrame({'Week': week_date, 'average_price': j})  # creating my dataframe with actual loop values
        df_list.append(df)  # holidng my dataframes for diffewrent dates

    df_final = pd.concat(df_list)
    df_final.reset_index(drop=True, inplace=True)  # created my final dataframe with two columns

    # convert list to series
    new_col_series = pd.Series(c_n)

    # insert new column into dataframe
    df_final.insert(loc=2, column='location', value=new_col_series)  # adding my location column
    df_final.iloc[:, [2, 1]] = df_final.iloc[:, [1, 2]].values  # swapping the columns to get output in expected format
    df_final = df_final.rename(columns={'Week': 'week', 'average_price': 'location',
                                        'location': 'average_price'})  # with values , column names should also be changed
    data_final_list.append(df_final)  # same appending to list
df_final_tables = pd.concat(data_final_list)
df_final_tables.reset_index(drop=True, inplace=True)  # making datframe
print(df_final_tables)  # the complete dataframe for all the years
df_final_tables['week'] = df_final_tables['week'].apply(convert_suitably)  # applying the function to entire column
df_final_tables.to_csv('Data of WEEKLY AVERAGE PRICES OF TOTAL TEA SOLD AT INDIAN AUCTION 2008-2023.csv',
                       index=False)  # converting it to csv
