import requests

url = 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=&city=100010000&page='
user_agents = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
cookies = '__zp_stoken__=b017eWFNVE3pISWIVMnBQLkwXZylscGlIRQU%2FbmAWd0sNKF0pdFkIVEVTLUJuDA0iLSZfXjgcejg6Ni83fTQDaHVfcXdPaUA5JURbeE8qeTdwQVhwM2FcUDkodxxRXCsqbx9tPzhnEEAKBTQ%3D; __a=14193959.1676375853.1678850441.1678872562.405.25.39.405; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fcity%3D100010000&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __c=1678872562; wbg=0; lastCity=100010000; _bl_uid=9dlXLewI4786IwwC0gsk0Omhe01a; wt2=D4nBd99oNUpM_32Wq3BPub4RlLBSGHYLkFo9XFr8OF3aPrxmVOpapLk9QmU9fPhwiNTQXBHku-W2xw880BXr4IA~~; __g=-; historyState=state; geek_zp_token=V1RNkmF-T53FduVtRvyBUQLiO47D3Twy4~; wd_guid=0af9d2c7-8f7e-4612-8ea7-ba2b1b91b05e'
headers = {'Referer': 'https://www.zhipin.com/web/geek/job?query='}
headers['user-agent'] = user_agents
headers['cookie'] = cookies

re = requests.get(url=url,headers=headers)

print(re.headers)

print(re.text)