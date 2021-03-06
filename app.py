from flask import Flask, request, abort

import urllib.request, json
import requests
from bs4 import BeautifulSoup

import os#
import sys
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

ACCESS_TOKEN= os.environ['ACCESS_TOKEN']
SECRET= os.environ['CHANNEL_SECRET']

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(SECRET)

pm_site = {}

@app.route("/")
def hello_world():
    return "hello world!"


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
#     _message = TextSendMessage(text='Nice to meet you!')
#     _message = TextSendMessage(text=(event.source.user_id)) #reply userid
#     line_bot_api.reply_message(event.reply_token, _message)  
    # message = TextSendMessage(text=event)
#     print(event)

    msg = event.message.text

# 爬搜尋引擎，預設爬回傳4筆
def get_search_engine(search_thing, result_num=4):
    result = []
    target_url = 'https://www.kham.com.tw/application/UTK01/UTK0101_03.aspx'
    target_param = urllib.parse.urlencode({'q':search_thing}) # Line bot 所接收的關鍵字 !!!!
    target = target_url + '?' + target_param
    r = requests.get(target)
    html_info = r.text # 抓取 HTML 文字
    soup = BeautifulSoup(html_info, 'html.parser')
    search_result = soup.find('ol', {'id': 'b_results'}) #搜尋所有結果
    search_result_li = search_result.find_all('li', {'class':'b_algo'}) # 每一則的結果
    for idx, li in enumerate(search_result_li):
        if idx < result_num:
            target_tag = li.find('h2').find('a') # 每一則的超連結
            title = target_tag.get_text() # 每一則的標題
            href= target_tag['href'] # 每一則的網址
            result.append((title, href))
    return result
        
            
import os
if __name__ == "__main__":

    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
