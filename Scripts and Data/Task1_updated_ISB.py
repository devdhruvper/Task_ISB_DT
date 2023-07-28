#Task1 - Dhruv Talan
#defining the function we will need to convert our date into the following fromat of dd-mm-yyy
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

def convert_suitably(data_str):
 date_obj = datetime.strptime(data_str, "%d/%m/%Y")
 new_date_str = date_obj.strftime("%d-%m-%Y")
 return new_date_str

data_final_list=[]
for year in range(2008,2024):

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

    # Getting the header names of the table using the first <tr> element and the header cells in it

    df = pd.DataFrame(columns=c_n)
    lencn = len(c_n)  # no of columns

    tr_all = second_table.find_all('tr')
    relevant_tr = tr_all[1:]

    cell = []
    for tr in relevant_tr:
        for row in tr.find_all('td'):
            for data in row.find_all('span'):
                cell.append(data.text)

    lencell = len(cell)  # represnts total no of cells in the table

    rows = [cell[i:i + lencn] for i in range(0, lencell, lencn)]


    r = pd.DataFrame(rows, columns=df.columns)
    df=pd.concat([df,r],ignore_index=True)
    df.reset_index(drop=True, inplace=True)

    df=df.drop(columns=['Tea Serve'],axis=0)
    df=pd.melt(df,id_vars=['Week Ending/Date'],var_name="location",value_name="average_price")
    df.rename(columns={'Week Ending/Date':'week'},inplace=True)
    data_final_list.append(df)
df_final_tables = pd.concat(data_final_list)
df_final_tables.reset_index(drop=True, inplace=True)#making datframe
print(df_final_tables) #the complete dataframe for all years
df_final_tables['week']=df_final_tables['week'].apply(convert_suitably) #applying the function to entire column
df_final_tables.to_csv('Data of WEEKLY AVERAGE PRICES OF TOTAL TEA SOLD AT INDIAN AUCTION 2008-2023.csv',index=False) #converting it to csv
