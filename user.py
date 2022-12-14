from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)
from bs4 import BeautifulSoup

from province import get_provinces, PROVINCES, get_case_for_province, get_top_10
import requests

PAGE_SIZE = 10

FIRST_PROMPT = TextSendMessage(text="Please select the information that you want to know.",
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="Overall", text="overall")),
        QuickReplyButton(action=MessageAction(label="Provinces", text="provinces")),
        QuickReplyButton(action=MessageAction(label="Top 10", text="top"))
    ]))

VALID_FIRST_CHOICE = ["overall", "provinces"]
OVERALL_THINGS = ["new_case","new_recovered","new_death","total_case","total_recovered","total_death","update_date"]

class User:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.first_choice = None
        self.province = None
        self.third_choice = None
        self.page = 0
    
    def handle_overall(self):
        x = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
        y = ""
        for info in OVERALL_THINGS:
            y += "{}: {}\n".format(info, x.json()[0][info])
        return TextSendMessage(text=y[:-1])

    def get_province_result(self, text):
        self.reset()
        result = get_case_for_province(text)
        x = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
        y = x.json()
        y = y[0]
        y = y["new_case"]
        z = "Last provinces update is : " + str(y)
        yo = "Number of cases: {}".format(result) + "\n" + z
        return TextSendMessage(text=yo)

    def handle_when(self):
        x = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
        y = x.json()[0]["txn_date"]
        z = "Last overall update is : " + str(y)
        return TextSendMessage(text=z) 

    def handle_whenp(self):
        x = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces')
        x = x.json()[0]
        y = ["txn_date"]
        z = "Last provinces update is : " + str(y)
        return TextSendMessage(text=z)

    def handle_province(self, text):
        provinces = get_provinces(self.page, PAGE_SIZE)

        if text == "next" and len(provinces) == PAGE_SIZE:
            self.page += 1
        elif text == "back" and self.page != 0:
            self.page -= 1
        elif text in PROVINCES:
            return self.get_province_result(text)
        
        items = []
        if self.page != 0:
            items.append(QuickReplyButton(action=MessageAction(label="Back", text="back")))
        for province in provinces:
            label = province
            if len(province) > 20 :
                label = "{}...".format(province[0:17])
            items.append(QuickReplyButton(action=MessageAction(label=label, text=province)))
        if len(provinces) == PAGE_SIZE:
            items.append(QuickReplyButton(action=MessageAction(label="Next", text="next")))

        return TextSendMessage(text="Please select province.",
            quick_reply=QuickReply(items=items))
    
    def get_response(self, text):
        if self.first_choice is None:
            if text == "overall":
                return self.handle_overall()
            elif text == "provinces":
                return TextSendMessage(text="NO!")
            elif text == "I am scared":
                return TextSendMessage(text="Don't be bro ;-)")
            elif text == "When":
                return self.handle_when()
            elif text == "when":
                return self.handle_when()
            elif text == "map":
                return TextSendMessage(text="https://covid19.th-stat.com/th/share/map")
            elif text == "Map":
                return TextSendMessage(text="https://covid19.th-stat.com/th/share/map")
            elif text == "Global" or text == "global":
                return TextSendMessage(text="No can't help you with that")
            elif text == "Whenp" or text == "whenp":
                return self.handle_whenp()
            elif text == "top":
                return TextSendMessage(text=get_top_10())
            else:
                return FIRST_PROMPT
        else:
            return self.handle_province(text)
