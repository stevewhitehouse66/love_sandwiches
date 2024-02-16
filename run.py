import gspread
from google.oauth2.service_account import Credentials



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales data input from user
    """
    while True:
        print('Please enter sales data from the last market')
        print('Data should be six numbers seperated by commas')
        print('Example: 10,20,30,40,50,60\n')
        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside try converts to integers
    Raises ValueError if stings cant be converted
    or if there aren't 6 values.
    """
    try:
        [int (value) for value in values]
        if len(values) != 6:
            raise ValueError(f'Exactly 6 values rquired, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid Data: {e}, please try again.\n')
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Update  data to new row on relevant worksheet
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'The {worksheet} worksheet was updated sucessfully...\n')


def calculate_surplus_data(sales_row):
    """
    Compare saleswith stock and calculate surplus
    - positive result indicates waste
    - negative result rquals extras made
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data=[]
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_five_entries_sales():
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item, adding 10%
    """
    print('Calculating stock data...\n')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data



def get_stock_values(data):
    stock_values = {}
    stock_data = SHEET.worksheet('stock').get_all_values()
    headings = stock_data[0]
    stock_row = stock_data[-1]
    stock_values = {heading: stock_row for heading, stock_row in zip(headings, stock_row)}
    print('Make the following sandwiches for the next market: ')
    
    return stock_values


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int (num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')
    stock_values = get_stock_values(stock_data)
    print(stock_values)

print('\nWelcome to Love Sandwiches Data Automation\n')
main()

