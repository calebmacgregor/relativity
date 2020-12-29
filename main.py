import requests
import json
from pprint import pprint

base_url = 'https://api.up.com.au/api/v1'
token = 'up:yeah:09mrmEuny7LbmCL2VUEBHf5Qwo8Lwp7He8X6nL1mOLs4nZxJZ61EyPFSpFi2DYKEidzw93qI5xOtdiA7iWowiRdsFGXuRAYLpiMg1XJHtLUwnEz0qpA3bbgvCNYZDlKw'
headers = {'Authorization' : 'Bearer ' + token}
transactional_account_id = '7f947112-89cd-4944-b9b3-818f39da7bc4'

#Set variables for income.
#To do: Set this dynamically based on the salary from the transaction data
hourly_wage = 29.8
minute_wage = hourly_wage / 60
daily_wage = hourly_wage * 8

#Build out my functions
def dollars_to_time(dollars, time):
    """
    Converts a dollar figure (taken as a float) into an time figure (returned as a float rounded to two decimal places)
    The second argument dictates what unit of time to use:
        'd' = day
        'h' = hour
        'm' = minute
    """
    if time == 'h':
        return round(dollars / hourly_wage, 2)
    elif time == 'm':
        return round(dollars / minute_wage, 2)
    elif time == 'd':
        return round(dollars / daily_wage, 2)

 

def get_accounts_and_balances(data):
    """
    Takes one argument (data) and returns the account names and balances for the up bank account
    Data should be the output of a get request to the /accounts/ url. For example:
        requests.get(base_url + '/accounts/', transactional_account_id, headers=headers)
    """
    accounts_and_balances = {}
    for i in data['data']:
        accounts_and_balances[i.get('attributes').get('displayName')] = i.get('attributes').get('balance').get('value')
    return accounts_and_balances

#Ping Up to get my account information
response = requests.get(base_url + '/accounts/', transactional_account_id, headers=headers)

data = response.json()

accounts_and_balances = get_accounts_and_balances(data)

# pprint(accounts_and_balances.values())
#Ping Up to get my transactional data
#To do: Get more than 10 records. Need to work out how pagination works.
transactions_request = requests.get(base_url + '/transactions', transactional_account_id, headers=headers)

transaction_data =  transactions_request.json()

transaction_amounts = [abs(float(i.get('attributes').get('amount').get('value'))) for i in transaction_data['data'] if i.get('attributes').get('description') != 'Round Up' and float(i.get('attributes').get('amount').get('value')) < 0]

total_spending = sum(transaction_amounts)

for i in transaction_data['data']:
    if i.get('attributes').get('description') != 'Round Up' and float(i.get('attributes').get('amount').get('value')) < 0:
        print(
            i.get('attributes').get('description'), 
            i.get('attributes').get('amount').get('value'),
            'This equates to approximately ' +  str(round(abs(float(i.get('attributes').get('amount').get('value'))) / minute_wage, 2)) + ' minutes of work'
            )

print(f'You have spent approximately {str(round(total_spending / minute_wage))} minutes of time ({str(round(total_spending / hourly_wage))} hours)')