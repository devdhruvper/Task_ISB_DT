
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

    for row in rows:
        r = pd.DataFrame([row], columns=df.columns)
        df = df.append(r, ignore_index=True)
