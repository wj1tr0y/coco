# coding = utf-8
import requests
import os
import time
def JoinLotteries(url):
    res = requests.get(url,headers=headers)
    # 获得抽奖列表 table
    table = res.json().get('data')
    url = 'https://lucky.nocode.com/lottery/{id}/join'
    for item in table:
        if item.get('joined') == False:
            res = requests.post(url.format(id=item.get('id')),headers=headers)
            if res.status_code == 200 and res.json().get('data') == True:
                print('成功参与抽奖：')
                prizes = item.get('prizes').get('data')
                for prize in prizes:
                    print(prize.get('name'))

def main():
    if os.path.exists('.config_luckynode'):
        with open('.config_luckynode', 'r') as f:
            headers['Authorization'] = f.readlines()[0]
    else:
        headers['Authorization'] = input("请输入你的Authorization值：")
        with open('.config_luckynode', 'w') as f:
            f.write(headers['Authorization'])
    print('正在参与公共福利抽奖...')
    JoinLotteries('https://lucky.nocode.com/public_lottery?page=1&size=5')
    for i in range(100):
        print('正在参与自助福利抽奖...')
        JoinLotteries('https://lucky.nocode.com/square')



if __name__ == '__main__':
    # 统一请求头
    headers = {}
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    main()