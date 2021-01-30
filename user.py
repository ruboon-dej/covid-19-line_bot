from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)
from bs4 import BeautifulSoup

from main import get_world_data

from province import get_provinces, PROVINCES, get_case_for_province

import requests

PAGE_SIZE = 10

FIRST_PROMPT = TextSendMessage(text="Please select the information that you want to know.",
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="Overall", text="overall")),
        QuickReplyButton(action=MessageAction(label="Provinces", text="provinces"))
    ]))

VALID_FIRST_CHOICE = ["overall", "provinces"]
OVERALL_THINGS = ["Confirmed","Recovered","Hospitalized","Deaths","NewConfirmed","NewRecovered","NewHospitalized","NewDeaths"]

class User:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.first_choice = None
        self.province = None
        self.third_choice = None
        self.page = 0
    
    def handle_overall(self):
        x = requests.get('https://covid19.th-stat.com/api/open/today')
        y = ""
        for info in OVERALL_THINGS:
            y += "{}: {}\n".format(info, x.json()[info])
        return TextSendMessage(text=y[:-1])

    def get_province_result(self, text):
        self.reset()
        result = get_case_for_province(text)
        return TextSendMessage(text="Number of cases: {}".format(result))

    def handle_when(self):
        x = requests.get('https://covid19.th-stat.com/api/open/today')
        y = x.json()["UpdateDate"]
        z = "Last overall update is : " + str(y)
        return TextSendMessage(text=z) 

    def handle_whenp(self):
        x = requests.get('https://covid19.th-stat.com/api/open/cases/sum')
        y = x.json()["LastData"]
        z = "Last provinces update is : " + str(y)
        return TextSendMessage(text=z)
    
    def cancel(self):
        self.reset
        return TextSendMessage(text="Done")

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
                self.first_choice = text
                return self.handle_province(text)
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
            elif text == "Cancel" or text == "cancel":
                return self.cancel()
            else:
                return FIRST_PROMPT
        else:
            return self.handle_province(text)
