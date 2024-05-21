import os
import secrets
import string
from line_bot_app.models import * #記得要改line_bot_app如果你和我不一樣

from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from module.langchain_tool import *
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import BaseTool

from django.conf import settings
from linebot import LineBotApi
from linebot.models import *
from urllib.parse import quote
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
db = SQLDatabase.from_uri("mysql+mysqlconnector://root:123456789@localhost:3306/my_project")
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = load_tools(["wikipedia"], llm=llm)
def MyAccount(event):
    flex_message = FlexSendMessage(
        alt_text='Flex_message',
        contents={
          "type": "bubble",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "我的帳本",
                "color": "#FFFFFF",
                "weight": "bold",
                "size": "xl"
              },
              {
                "type": "text",
                "text": "請選擇要進行的操作",
                "color": "#FFFFFF",
                "weight": "regular"
              }
            ]
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "uri": "https://liff.line.me/2004983305-Wxv3l2rx",
                  "label": "記帳"
                }
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "查詢帳本",
                  "uri": "https://liff.line.me/2004983305-2LqXBLZr"
                }
              }
            ]
          },
          "styles": {
            "header": {
              "backgroundColor": "#00B900"
            }
          }
        }
    )
    line_bot_api.reply_message(event.reply_token, flex_message)



def manageForm(event, mtext, user_id):  # 處理LIFF傳回的from資料
  try:
    flist = mtext[3:].split('/')  # 去除前三個#再分解字串
    User_imput = flist[0]  # 取得輸入資料


    text1 = User_imput
    message = TextSendMessage(
      text=text1
    )
    line_bot_api.reply_message(event.reply_token, message)

  except:
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤'))


def Form(event, text,user_id):

  category = text.split(',')[0].split(':')[1].strip().strip('"')
  amount = int(text.split(',')[1].split(':')[1].strip().strip('"'))
  item = text.split(',')[2].split(':')[1].strip().strip('"')
  location = text.split(',')[3].split(':')[1].strip().strip('"')
  transaction_type = text.split(',')[4].split(':')[1].strip().strip('"')
  #print(location)
  query_params = {
    "category": category,
    "amount": amount,
    "item": item,
    "location": location,
    "transaction_type": transaction_type,
    "user_id": user_id
  }
  query_params_encoded = {key: quote(str(value)) for key, value in query_params.items()}

  query_string = "&".join([f"{key}={value}" for key, value in query_params_encoded.items()])
  url = f"https://line-lift-form.vercel.app?{query_string}"

  flex_message = FlexSendMessage(
    alt_text='Flex_message',
    contents={
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "選單",
            "color": "#FFFFFF",
            "weight": "bold",
            "size": "xl"
          },
          {
            "type": "text",
            "text": "請完成選單",
            "color": "#FFFFFF",
            "weight": "regular"
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "uri": url,
              "label": "選單內容"
            }
          },
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#00B900"
        }
      }
    }
  )
  line_bot_api.reply_message(event.reply_token, flex_message)

def creategroup(event):
    flex_message = FlexSendMessage(
      alt_text='Flex_message',
      contents={
        "type": "bubble",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "創建群組",
              "color": "#FFFFFF",
              "weight": "bold",
              "size": "xl"
            },
          ]
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "uri": "https://liff.line.me/2004983305-yZblg4aW",
                "label": "創建"
              }
            }
          ]
        },
        "styles": {
          "header": {
            "backgroundColor": "#00B900"
          }
        }
      }
    )
    line_bot_api.reply_message(event.reply_token, flex_message)
#創建群組
def CreateGroup(mtext,user_id):
    temp = mtext[6:]#取得井字號的後面
    letters = string.ascii_letters#產生英文字母
    digits = string.digits#產生字串
    # 如果有和資料庫重複會重新生成
    while True:
        secure_random_string = ''.join(secrets.choice(letters) + secrets.choice(digits) for i in range(15))#數字和英文字母串接
        if not GroupTable.objects.filter(group_code=secure_random_string).exists():
            break
    group_name = temp
    group_code = secure_random_string
    try:
        #剛創建的群組加入資料庫
        unit = GroupTable(group_name=group_name, group_code=group_code)
        unit.save()
        #抓取群組的id且把資料加入到linking table中
        group = GroupTable.objects.get(group_id=unit.group_id)
        user_instance = PersonalTable.objects.get(personal_id=user_id)
        try:
            unit3 = PersonalGroupLinkingTable.objects.create(personal=user_instance,group=group)
            return '成功創建群組'
        except Exception as e:
            print(f"Error creating linking table record: {e}")
    except Exception as e:
        print(f"Error creating group: {e}")
#joingroup的flex
def joingroup(event):
    flex_message = FlexSendMessage(
      alt_text='Flex_message',
      contents={
        "type": "bubble",
        "header": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "加入群組",
              "color": "#FFFFFF",
              "weight": "bold",
              "size": "xl"
            },
          ]
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "uri",
                "uri": "https://liff.line.me/2004983305-RQ7w3gVM",
                "label": "加入"
              }
            }
          ]
        },
        "styles": {
          "header": {
            "backgroundColor": "#00B900"
          }
        }
      }
    )
    line_bot_api.reply_message(event.reply_token, flex_message)
#加入群組
def JoinGroup(mtext, user_id):
    code = mtext[6:]  # 取得井字號的後面
    #判斷使用者輸入有無此群組
    unit2 = GroupTable.objects.filter(group_code=code)
    if not unit2:
        return '查無此群組，請重新輸入'
    else:
        # 判斷使用者是否有想要重複加入群組，去linkingtable看有沒有重複加入
        group = GroupTable.objects.get(group_code=code)
        user_instance = PersonalTable.objects.get(personal_id=user_id)
        unit4 = PersonalGroupLinkingTable.objects.filter(personal=user_instance, group=group)
        if unit4:
            return '已經有加入該群組，若是要加入新群組請重新核對您的群組代碼'
        else:
            try:
                user_instance = PersonalTable.objects.get(personal_id=user_id)
                unit5 = PersonalGroupLinkingTable.objects.create(personal=user_instance,group=group)
                return '成功加入群組'
            except Exception as e:
                print(f"Error creating linking table record: {e}")
                return '加入群組時發生錯誤，請稍後再試'
def classfication(text,user_id,transaction_type):
    user_category=PersonalCategoryTable.objects.filter(personal_id=user_id,transaction_type=transaction_type)
    user_category_set=[]
    for category in user_category:
        category_data = {
            "personal_category_id": category.personal_category_id,
            "category_name": category.category_name,
            "category_description": category.category_description,
        }
        user_category_set.append(category_data)
    agent = get_account_classification_tool(llm)
    print(agent(f"使用者類別：{user_category_set}，使用者輸入：{text}"))

def get_account_classification_tool(llm):
    tools = [account_classification()]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True)
