fortnightly_salary = {}

# for page in results:
#     for i in page['data']:
#         if i.get('attributes').get('rawText') == 'Youi Salaries Ac':
#             pprint(i)
#             #Format the date into something reasonable
#             #To do: Need to handle timezones properly for this, currently based on Melbourne time I think
#             date = iso8601.parse_date(i.get('attributes').get('createdAt')).strftime('%d/%m/%Y %H:%M:%S')
#             value = i.get('attributes').get('amount').get('value')
#             fortnightly_salary[date] = value

print(fortnightly_salary)
