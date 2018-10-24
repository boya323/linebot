from flask import Flask, request, abort
import os
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

to=U484944ffc0e2f541b7e21ca8fb3a00d7


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
    message = TextSendMessage(text='哈囉！你好！')
    message2 = TextSendMessage(event.source.user_id)
    line_bot_api.reply_message(event.reply_token, [message , message2])
import os

#PUSH 文字
line_bot_api.push_message(to,TextSendMessage(text=':):):)'))


#PUSH 圖片
img_message = ImageSendMessage(
 original_content_url='https://i.imgur.com/NzVD7st.png',
 preview_image_url ='https://i.imgur.com/NzVD7st.png'
)
line_bot_api.push_message(to,img_message)

#PUSH 貼圖
line_bot_api.push_message(to,StickerSendMessage(package_id='180' ,sticker_id='3'))

#PUSH 按鈕
confirm_temp_message = TemplateSendMessage(
 alt_text='小熊軟糖好吃',
 template=ConfirmTemplate(
  text='小熊軟糖好吃',
  actions=[
   PostbackTemplateAction(
    label='是',
    text='是',
    data='yes'),
   MessageTemplateAction(
    label='否',
    text='否')
   ]
  )
 )

line_bot_api.push_message(to,confirm_temp_message)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
