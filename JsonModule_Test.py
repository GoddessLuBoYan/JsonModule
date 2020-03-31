import json
from JsonModule import Json

d = {
    "x":1.2,
    "y":"2",
    "z":[5,6,7],
    "w":{
        "a":1,
        "b":None,
        "c":False
    }
}

print(d)

input("点击序列化")

json_str1 = Json.dumps(d)
json_str2 = json.dumps(d)

print(json_str1)
print(json_str2)
print("json_str1", "==" if json_str1 == json_str2 else "!=", "json_str2")

input("点击反序列化")

d1 = Json.loads(json_str1)
d2 = json.loads(json_str2)
print(d1)
print(d2)
print("d1", "==" if d1 == d2 else "!=", "d2")

input("请按回车退出程序")