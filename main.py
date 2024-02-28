import logging
import os
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import excel_method, requests
from config import goods, home, initial
from methods import order

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前路径

logging.basicConfig(level=logging.INFO)


# 创建一个 Pydantic 模型来定义请求体的结构
class OrderData(BaseModel):
    buy_number: int
    desc: str
    goods_price: float
    goods_title: str
    notes: str
    phone_number: str
    tag: str
    state:str
    open_id:str

# buy_number: 4
# desc: "灵力价"
# goods_price: 32.99
# goods_title: "小A"
# notes: ""
# phone_number: "17777253073"
# tag: "小A"

# 定义一个接收 POST 请求的路由，接收请求体中的数据
@app.post("/service_order/")
async def service_order(order_data: OrderData):
    # 获取请求体中的数据
    buy_number = order_data.buy_number
    desc = order_data.desc
    goods_price = order_data.goods_price
    goods_title = order_data.goods_title
    notes = order_data.notes
    phone_number = order_data.phone_number
    tag = order_data.tag
    state = order_data.state
    open_id = order_data.open_id

    order_number = order.generate_order_id()

    # 在这里可以对数据进行进一步处理，比如存储到数据库中或者进行其他业务逻辑处理
    excel_method.order(file_path='excel_data/service_order.xlsx', v=[order_number,state,open_id,
                                                                     buy_number, desc, goods_price, goods_title, notes,
                                                                     phone_number, tag]
                       )
    # 返回接收到的数据
    return {
        "order_number": order_number,
        "buy_number": buy_number,
        "desc": desc,
        "goods_price": goods_price,
        "goods_title": goods_title,
        "notes": notes,
        "phone_number": phone_number,
        "tag": tag
    }


class Openid(BaseModel):
    openid: str


@app.post("/op_id/")
async def receive_openid(openid_data: Openid):
    code = openid_data.openid
    # 在这里你可以处理接收到的 openid，比如保存到数据库中等操作
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': 'wx549c0fa1cd5e49a7',
        'secret': '822e1e21cb7dc1cfeaa3eb3bfdfe9547',
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data is None:
        data = "None"
    # 获取用户的 openid
    openid = data.get('openid')
    session_key = data.get('session_key')
    print(data, code)
    v = [openid, session_key, code]
    try:
        unionid = data.get('unionid')
        v.append(unionid)
    except:
        pass

    excel_method.order(file_path='excel_data/user_info.xlsx', v=v)
    return {"message": "Received openid successfully", "openid": openid}


@app.post("/coupon")
async def receive_op():
    return "True"





@app.get("/get_image/{name:path}")
async def get_image(name: str):
    # 根据产品名称构建图片文件名
    image_filename = f"{name}"
    # 图片文件的完整路径
    image_path = os.path.join(current_dir, "images", image_filename)
    # 返回图片文件
    return FileResponse(image_path)


@app.get("/goods_list", response_model=List[dict])
async def get_product():
    return_goods = goods.goods
    modified_goods = []
    for i in return_goods:
        modified_good = i.copy()
        modified_good["pic_url"] = initial.Server_ImageUrl + '/product/' + i["pic_url"]
        modified_goods.append(modified_good)
    return modified_goods


@app.get("/get_banner", response_model=List)
async def get_banner():
    return home.banner





@app.get("/get_category", response_model=List[dict])
async def get_category():
    return home.categories


@app.get("/home_initial", response_model=dict)
async def home_initial():
    return home.initial_data
