# import requests
from province import get_top_10
# res = requests.get('https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data')
get_top_10()
# from bs4 import BeautifulSoup

# class Data:
#     def __init__(self, name, cases, deaths, recoveries):
#         self.name = name
#         self.cases = cases
#         self.deaths = deaths
#         self.recoveries = recoveries
#     def __str__(self):
#         return "Location: {}\nCases: {}\nDeaths: {}\nRecoveries: {}\n".format(self.name, self.cases, self.deaths, self.recoveries)


# def get_world_data(limit=5):
#     soup = BeautifulSoup(res.content, 'html.parser')
#     table = soup.select("#thetable")[0]
#     world = table.find(class_="sorttop")

#     data = []
#     world_values = world.find_all("th")[1:5]
#     data.append(Data(world_values[0].text[:-4], world_values[1].text[:-1], world_values[2].text[:-1], world_values[3].text[:-1]))
#     rows = table.find_all("tr")
#     for row in rows[:limit]:
#         name = row.find("a")
#         values = row.find_all("td")[0:3]

#         if len(values) == 3:
#             data.append(Data(name.text, values[0].text[:-1], values[1].text[:-1], values[2].text[:-1]))
#     p = ""
#     for d in data:
#         p += str(d) + "\n"
#     return TextSendMessage(text=p)
