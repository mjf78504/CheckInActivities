# -*- coding: utf-8 -*-
"""
#  ChinaUnicom.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/3
@Software   : PyCharm
"""
import requests
import time
import random
import re
from base64 import b64encode
from libs.encrypto import rsa_encrypt_CU,pad_randomstr_CU


pubKey_CU = ('-----BEGIN PUBLIC KEY-----\n'
                 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6'
                 'FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9'
                 'NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0Srctg'
                 'aqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB\n'
                 '-----END PUBLIC KEY-----')


class ChinaUnicomApp:
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'User-Agent': 'ChinaUnicom4.x/70 CFNetwork/811.5.4 Darwin/16.7.0',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate',
        }
        self.token = ''
        self.phoneNum = ''
        self.areaCode = ''


    def login_CU(self, username, password):
        self.phoneNum = username
        username_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(username, size=6)))
        password_CU = b64encode(rsa_encrypt_CU(pubKey_CU, pad_randomstr_CU(password, size=6)))
        cur_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.headers['Host'] = 'm.client.10010.com'
        self.data = {
            'version': 'iphone_c@5.7',
            'mobile': username_CU,
            'netWay': 'wifi',
            'isRemberPwd': 'true',
            'appId': '81740c90c669bda467dec2d09551b684e4e61006d6caebe41a45689995edc187',
            'deviceId': 'c65f20c8d6d2136065aa52a56ff80e8d325084b9d43aaa5d7a06e2f22894005d',
            'pip': '',
            'password': password_CU,
            'deviceOS': '10.3.3',
            'deviceBrand': 'iphone',
            'deviceModel': 'iPhone',
            'keyVersion': '1',
            'deviceCode': 'EE0D86F7-79C1-42CF-8D63-543EC7F1DCC3',
        }

        login_url = 'http://m.client.10010.com/mobileService/login.htm'
        # Host 请求尝试次数
        n = 3
        while n:
            try:
                login_req = self.session.post(login_url, headers=self.headers, data=self.data)
                if login_req.json()['code'] == '0':
                    self.token = self.session.cookies.get('a_token', '')
                    self.areaCode = self.session.cookies.get('u_areaCode', '')
                    content_login = cur_time1 + ' 联通APP签到：\n'
                    return 1, content_login
                else:
                    print(cur_time1 + ' 联通APP登陆失败...')
                    content_login = cur_time1 + '  自动签到任务失败\n' + '错误原因：APP登陆失败...\n'
                    return 0, content_login
            except Exception as err:
                print(err)
                time.sleep(5)
                n -= 1
                print('尝试重复请求...')
                continue
        content_login = cur_time1 + '  自动签到任务失败\n' + '错误原因：二次 Host 请求失败...\n'
        return -1, content_login

    def signin_CU(self):
        try:
            cur_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.headers['Host'] = 'act.10010.com'
            # cookie = self.session.cookies
            token = '?token=' + self.session.cookies.get('a_token', '')
            # 进入每日签到活动, cookies=self.session.cookies
            query_url = 'http://act.10010.com/SigninApp/signin/querySigninActivity.htm'
            self.session.get(url=query_url+token, headers=self.headers)
            # 检查是否已签到
            isSignin_url = 'http://act.10010.com/SigninApp/signin/rewardReminder.do'
            isSignin_req = self.session.post(url=isSignin_url, headers=self.headers)
            # 进行签到/取消签到
            signin_url = 'http://act.10010.com/SigninApp/signin/daySign.do'
            if int(isSignin_req.json()['todayIsSignin']):
                signin_req = self.session.post(url=signin_url)
                dailyCoin = signin_req.json()['prizeCount']
                print('今日获得金币：' + dailyCoin)
            else:
                dailyCoin = '今日已签到过'
                print(dailyCoin)
            # 获取总金币
            gold_url = 'http://act.10010.com/SigninApp/signin/goldTotal.do'
            gold_req = self.session.post(url=gold_url)
            totalCoin = gold_req.json()#['goldTotal']
            # 任务测试
            task01_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA395307980'
            task01_req = self.session.get(url=task01_url)
            print(task01_req.text)
            task02_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA930618570'
            task02_req = self.session.get(url=task01_url)
            print(task02_req.text)
            task03_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA643311145'
            task03_req = self.session.get(url=task01_url)
            print(task03_req.text)
            task04_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA29407319'
            task04_req = self.session.get(url=task01_url)
            print(task04_req.text)
            task05_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA158495857'
            task05_req = self.session.get(url=task01_url)
            print(task05_req.text)
            task06_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA705553092'
            task06_req = self.session.get(url=task01_url)
            print(task06_req.text)
            task07_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA590934984'
            task07_req = self.session.get(url=task01_url)
            print(task07_req.text)
            task08_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA353776054'
            task08_req = self.session.get(url=task01_url)
            print(task08_req.text)
            task09_url = 'https://act.10010.com/SigninApp/task/taskQuantityAccumulative.do?taskCode=TA52554375'
            task09_req = self.session.get(url=task01_url)
            print(task09_req.text)
            exit()
            # 每日免费抽奖
            print('---每天免费抽奖三次情况记录---')
            usernumberofjsp_url = 'http://m.client.10010.com/dailylottery/static/textdl/userLogin'
            usernumberofjsp_req = self.session.get(url=usernumberofjsp_url).text
            usernumberofjsp_search = re.search(r'[a-zA-Z0-9]{32}',usernumberofjsp_req).group()
            lottery_url = 'https://m.client.10010.com/dailylottery/static/doubleball/choujiang?usernumberofjsp=' + usernumberofjsp_search
            for i in range(1,4):
                lottery_req = self.session.post(url=lottery_url).json()
                print(lottery_req['RspMsg'])
            # 访问访问Weibo获取金币
            print('---访问微博一次获取1个金币(每天一次)---')
            weibo_url = 'https://act.10010.com/signinAppH/commonTask'
            weibo_data = {
                'transId': str(time.strftime('%Y%m%d%H%M')) + '3.96133858168' + str(random.randint(0000,9999)),
                'userNumber': self.phoneNum,
                'taskCode': 'TA590934984',
                'finishTime': '20200102221522',
                'taskType': 'DAILY_TASK',
            }
            gold_req = self.session.post(url=weibo_url, data=weibo_data)
            print(gold_req.json()['respMessage'])
            # 获取执行前成长值
            growth_url = 'https://m.client.10010.com/growthfunction/queryGrowScore.htm'
            oldgrowth_req = self.session.post(url=growth_url)
            oldgrowthV = oldgrowth_req.json()['data']['growthV']
            # 点赞获取成长值
            like_url = 'https://m.client.10010.com/commentSystem/csPraise'
            like_data = {
                'pointChannel': '01',
                'pointType': '01',
                'reqChannel': 'quickNews',
                'reqId': '35955a274f7e40f587af629e71a0f9a4',
            }
            print('---点赞一次获取1个成长值(每天三次)---')
            for i in range(1,4):
                like_req = self.session.post(url=like_url, data=like_data)
                likestatus = like_req.json()
                print(likestatus['desc'])
            # 评论获取成长值
            reply_url = 'https://m.client.10010.com/commentSystem/saveComment'
            reply_data = {
                'id': '35955a274f7e40f587af629e71a0f9a4',
                'newsTitle': '少年，不拼你就“chong”一把',
                'commentContent': '联通福利好，支持联通！',
                'upLoadImgName': '',
                'reqChannel': 'quickNews',
                'subTitle': '充值就享9折优惠，还有视频会员福利！',
                'belongPro': '098',
                'mainImage': 'https://m1.img.10010.com/resources/noticeSys/20191220/jpg/938ddad309ff421bba691a0695410f73.jpg',
            }
            print('---评论一次获取2个成长值(每天三次)---')
            for i in range(1,4):
                reply_req = self.session.post(url=reply_url, data=reply_data)
                replystatus = reply_req.json()
                print(replystatus['desc'])
            # 分享获取成长值+金币
            share_url = 'https://m.client.10010.com/mobileService/customer/quickNews/shareSuccess.htm'
            list_url = 'https://m.client.10010.com/commentSystem/getNewsList'
            start_sec = int(1576944000)
            end_sec = int(time.time())
            work_days = int((end_sec - start_sec)/(24*60*60))
            list_data = {
                'pageNum': work_days,
                'pageSize': '10',
                'reqChannel': '00',
            }
            print('---分享一次获取2个成长值(每天三次)---')
            print('---分享一次获取2个金币(每天十次)---')
            list_req = self.session.post(url=list_url, data=list_data).json()
            for list_id in list_req['data']:
                share_data = {
                    'newsId': list_id['id'],
                }
                share_req = self.session.post(url=share_url, data=share_data)
                sharestatus = share_req.json()
                print(sharestatus['desc'])
            # 获取执行后成长值
            nowgrowth_req = self.session.post(url=growth_url)
            nowgrowthV = nowgrowth_req.json()['data']['growthV']
            print('---成长值情况记录---')
            print('执行前成长值：' + oldgrowthV)
            print('执行后成长值：' + nowgrowthV)
            # 获取签到历史
            print('---签到情况记录---')
            querySignin_url = 'http://act.10010.com/SigninApp/mySignin/querySignin.do'
            querySignin_req = self.session.post(url=querySignin_url)
            continuCount = querySignin_req.json()['continuCount']
            signinDateList = ', '.join(querySignin_req.json()['signinDateList'])
            content_signin = '连续签到天数：' + continuCount + '\n' + '今日获得金币：' + dailyCoin + '\n' + '签到获得总金币：' + totalCoin + '\n' + '签到历史：' + signinDateList
            print(cur_time2 + ' APP签到成功...\n' + content_signin)
            return True, content_signin
        except Exception as err:
            print(cur_time2 + ' APP签到失败...\n失败原因：' + str(err))
            content_signin = 'APP签到失败' + str(err)
            return False, content_signin

    def woTree(self):
        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.headers['Host'] = 'm.client.10010.com'
        getAct_url = 'http://m.client.10010.com/mactivity/arborday/index'  # GET
        getAct = self.session.get(url=getAct_url, headers=self.headers)
        # TODO 分析html中的 <div class="jingyanzhi">

        data = {
            'url': getAct_url,
            'serviceCode': 'takeActivityInfo',
            'channel': 'mobileClient',
            'city': self.areaCode,
            'transId': times,
            'phoneNum': self.phoneNum,
        }
        takeAct_url = 'http://m.client.10010.com/freegift-interface/appUrlShare/takeActivityInfo'  # POST
        takeAct = self.session.post(url=takeAct_url, headers=self.headers, data=data)
        watering_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/0/1/grow'  # POST
        weed_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/1/1/grow'
        deinsec_url = 'http://m.client.10010.com/mactivity/arborday/arbor/1/2/1/grow'
        watering = self.session.post(url=watering_url, headers=self.headers)
        wateringStates = watering.json()['addedValue']
        weed = self.session.post(url=weed_url, headers=self.headers)
        weedStates = weed.json()['addedValue']
        deinsec = self.session.post(url=deinsec_url, headers=self.headers)
        deinsecStates = deinsec.json()['addedValue']

        content = "\n{} 沃之树：\n    浇水：{}次\n    除草：{}次\n    除虫：{}次\n".format(
            cur_time, wateringStates, weedStates, deinsecStates)
        print(content)
        return 1, content

    def woRight(self):
        qy_url = 'https://m.client.10010.com/mobileService/openPlatform/openPlatLine.htm?to_url=https://qy.chinaunicom.cn/mobile/auth/index'
        qy_data = {
            'yw_code': '',
            'desmobile': self.phoneNum,
            'version': 'android@7.0100',
        }
        qy_req = self.session.post(url=qy_url, data=qy_data, allow_redirects=False).headers['Location']
        self.session.cookies.clear()
        print(self.session.cookies.get_dict())
        account_url = 'https://qy.chinaunicom.cn/mobile/auth/getAccountByCookie'
        qy_cookies = self.session.get(url=account_url)
        self.session.cookies.set('remember_me','d14d7880-ec2c-49fa-898d-2afb61bdeb4e')
        qylogin_req = self.session.get(url=qy_req)
        # 权益中心首页礼品
        qyhome_url = 'https://qy.chinaunicom.cn/mobile/lottery/doLo?actId=1000000000012802'
        qyhome_msg = self.session.get(url=qyhome_url).json()
        print(qyhome_msg)
        # 权益中心签到
        qysign_url = 'https://qy.chinaunicom.cn/mobile/actsign/checkAccSign'
        qysign_msg = self.session.get(url=qysign_url).json()['resMsg']
        print(qysign_msg)
        return 1, qysign_msg
