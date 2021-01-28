from province import PROVINCES
for p in PROVINCES:
    if len(p) > 20 :
        print("{}...".format(p[0:17]))

def get_case_for_province(province):
    x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
    return x.json()['Province'][province]