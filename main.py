from flask import Flask, request, abort
from datetime import datetime
import get_news
# import requests
import os
import io
import pred
from PIL import Image
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, TextMessage
from linebot.models import ImageMessage, TextSendMessage
from google.cloud import storage

app = Flask(__name__)
GCS_BUCKET = 'your GCS bucket name'
storage_client = storage.Client()
bucket = storage_client.get_bucket(GCS_BUCKET)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(FollowEvent)
def on_follow(event):
    reply_token = event.reply_to
    user_id = event.source.user
    profiles = line_bot_api.get_proSune(user_id=user_id)
    display_name = profiles.displaySUNname
    top_message = display_name + "さんフォローありがとう!"

    line_bot_api.reply_messag(
        reply_token=reply_token,
        messages=TextSendMessage(text=top_message)
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.type == "message":
        if (event.message.text == "yahoo!") or (event.message.text == "ヤフー") or (event.message.text == "news") or (event.message.text == "ニュース"):
            news, url = get_news.get_news()
            topics1 = "1 :" + news[0] + "\n<<" + url[0] + ">>"
            topics2 = "2 :" + news[1] + "\n<<" + url[1] + ">>"
            topics3 = "3 :" + news[2] + "\n<<" + url[2] + ">>"
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="現在時刻のyahoo!news topic top3を表示します！"),
                    TextSendMessage(text=topics1),
                    TextSendMessage(text=topics2),
                    TextSendMessage(text=topics3),
                    # TextSendMessage(text=url[2]),
                    # TextSendMessage(text=news[2]),
                    # TextSendMessage(text=url[2]),
                ]
            )
        if (event.message.text == "こんにちは") or (event.message.text == "こんにちは!") or (event.message.text =="ハロー"):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="こんにちは！"))
        if (event.message.text == "ありがとう") or (event.message.text == "ありがとう!") or (event.message.text =="さんきゅー"):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="どういたしまして！"))
        if (event.message.text == "暇") or (event.message.text == "コロナでヒマ") or (event.message.text =="コロナで暇"):
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="勉強しましょう。"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="まだその言葉は教えてもらってないんです.覚えます！"+ chr(0x100029) + chr(0x100098)))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):

    message_id = event.message.id

    img_path, img_name = save_image(message_id)
    # img_mo = getImage(img_path, img_name, model_path)

    # result = line_bot_api.get_message_content(message_id)

    # line_bot_api.reply_message(event.reply_token, image_message)

    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text="ok")
        ]
    )


def save_image(message_id):
    """保存"""
    message_content = line_bot_api.get_message_content(message_id)
    time = datetime.now().strftime('%M_%S')
    bio = io.BytesIO()
    img = Image.open(io.BytesIO(message_content.content))
    pre = pred.pred(img)
    img.save(bio, format='png')
    path = 'num/test{}.png'.format(time)
    name = 'test{}.png'.format(time)
    blob = storage.Blob(path, bucket)
    blob.upload_from_string(data=bio.getvalue(), content_type="image/png")

    return path, name


if __name__ == "__main__":
   app.run(host='127.0.0.1', port=8080, debug=True)