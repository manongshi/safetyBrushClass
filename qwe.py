import requests

cookies = {
    '__root_domain_v': '.mycourse.cn',
    '_qddaz': 'QD.327341573812478',
    'lastSE': 'bing',
    'Hm_lvt_05399ccffcee10764eab39735c54698f': '1741573810,1741664953',
    'HMACCOUNT': '11872E5387C7BA9E',
    'Hm_lpvt_05399ccffcee10764eab39735c54698f': '1741697959',
    '_qddab': '3-dcl4i.m84hzxbv',
    'SERVERID': '9ee29c682be9356b7648e0eed94165c1|1741701692|1741701687',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://weiban.mycourse.cn',
    'priority': 'u=1, i',
    'referer': 'https://weiban.mycourse.cn/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-token': '6a2f43d8-c1e3-416b-bf69-485cd3aee660',
    # 'cookie': '__root_domain_v=.mycourse.cn; _qddaz=QD.327341573812478; lastSE=bing; Hm_lvt_05399ccffcee10764eab39735c54698f=1741573810,1741664953; HMACCOUNT=11872E5387C7BA9E; Hm_lpvt_05399ccffcee10764eab39735c54698f=1741697959; _qddab=3-dcl4i.m84hzxbv; SERVERID=9ee29c682be9356b7648e0eed94165c1|1741701692|1741701687',
}

params = {
    'timestamp': '1741701570.907',
}

data = {
    'tenantCode': '65000003',
    'userId': '2f98aa78-efb9-44cf-8d45-acf2355be1f0',
    'ended': '2',
}

response = requests.post(
    'https://weiban.mycourse.cn/pharos/index/listMyProject.do',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
).content.decode()
print(response)