import requests
x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
key = 'Samut Sakhon'
result = x.json()['Province'][key]

print(result)