from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)

from province import get_provinces, PROVINCES, get_case_for_province

import requests

PAGE_SIZE = 10

FIRST_PROMPT = TextSendMessage(text="Please select the second choice",
    quick_reply=QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="Overall", text="overall")),
        QuickReplyButton(action=MessageAction(label="Provinces", text="provinces"))
    ]))

VALID_FIRST_CHOICE = ["overall", "provinces"]

class User:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.first_choice = None
        self.province = None
        self.third_choice = None
        self.page = 0
    
    def handle_overall(self):
        pass

    def get_province_result(self, text):
        self.reset()
        result = get_case_for_province(text)
        return TextSendMessage(text="Number of cases: {}".format(result))

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

        return TextSendMessage(text="Please select the second choice",
            quick_reply=QuickReply(items=items))
    
    def get_response(self, text):
        x = requests.get('https://covid19.th-stat.com/api/open/today')
        if self.first_choice is None:
            if text == "overall":
                return self.handle_overall()
            elif text == "provinces":
                self.first_choice = text
                return self.handle_province(text)
            else:
                return FIRST_PROMPT
        else:
            return self.handle_province(text)

            


    def overall_cases():
        pass
