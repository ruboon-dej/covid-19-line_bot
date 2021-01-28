from province import PROVINCES
import requests

OVERALL_THINGS = ["Confirmed","Recovered","Hospitalized","Deaths","NewConfirmed","NewRecovered","NewHospitalized","NewDeaths"]
# for p in PROVINCES:
#     if len(p) > 20 :
#         print("{}...".format(p[0:17]))

# def get_case_for_province(province):
#     x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
#     return x.json()['Province'][province]

# def handle_overall(self):
#     x = requests.get('https://covid19.th-stat.com/th/apim')
#     y = ""
#     for info in OVERALL_THINGS:
#         y += "{}: {}\n".format(info, x.json()[info])
#     return TextSendMessage(text=y)


x = requests.get('https://covid19.th-stat.com/api/open/today')
y = ""
for info in OVERALL_THINGS:
    y += "{}: {}\n".format(info, x.json()[info])
print (y)