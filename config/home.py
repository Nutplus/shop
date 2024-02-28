from config import initial

url_banner = initial.Server_ImageUrl + "/home/"
url_categories = initial.Server_ImageUrl + "/categories/"

banner = [
    url_banner + 'banner1.jpg',
    url_banner + 'banner2.jpg',
    url_banner + 'banner3.png'

]

# banner元素直接完整URL，
# 图片大小 高480 宽250

categories = [
    {"id": 1, "name": "分类1", "icon": url_categories + "1.png"},
    {"id": 2, "name": "分类2", "icon": url_categories + "2.png"},
    {"id": 3, "name": "分类3", "icon": url_categories + "3.png"},
    {"id": 4, "name": "分类4", "icon": url_categories + "4.png"},
    {"id": 5, "name": "分类3", "icon": url_categories + "5.png"},
    {"id": 6, "name": "分类3", "icon": url_categories + "6.png"},
    {"id": 7, "name": "分类3", "icon": url_categories + "7.png"},
    {"id": 8, "name": "分类3", "icon": url_categories + "8.png"},
    {"id": 9, "name": "分类3", "icon": url_categories + "9.png"},
    {"id": 10, "name": "分类3", "icon": url_categories + "10.png"}
]
initial_data = {
    'goodsDynamic': [
        {'avatarUrl': '/static/images/categorie/1.png', 'nick': 'A', 'goodsName': 'B'},
        {'avatarUrl': '/static/images/categorie/1.png', 'nick': 'B', 'goodsName': 'A'},
    ],
    'show_buy_dynamic': '1'
}
