# ！ zap没有重放请求的api只有gui界面的编辑重放请求，但是可以通过结合python的request模块做到在此处修改请求并重放
from zapv2 import ZAPv2
import requests

# 创建zap api实例
zap = ZAPv2(apikey='nhocra6st486sshpdb54b2eopp', proxies={'http': 'http://127.0.0.1:9999'})

# 当前zap抓到的历史请求，用baseurl筛出要重放的根域名
history = zap.core.messages(baseurl='https://jzapi.daojia.com')

for message in history:
    # print(message['requestHeader'])

    url = message['requestHeader'].split(' ')[1]
    print(url)

    # 构造新的请求头
    headers = {}
    for line in message['requestHeader'].split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value.strip()

    # 修改请求头字段
    headers['Custom-Header'] = 'CustomValue'
    print(headers)
    print('---')

    # 重放请求
    response = requests.get(url, headers=headers)
    print(response.text)
    print('============================================================')
