import os
import random
import pymongo
import requests
from flask import Flask,jsonify,request,render_template
import json
import time
import JiaM
import ddddocr
app = Flask(__name__)
headers = {
    # 'accept': 'application/json, text/plain, */*',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'cookie': 'Hm_lvt_05399ccffcee10764eab39735c54698f=1728354142; Hm_lpvt_05399ccffcee10764eab39735c54698f=1728368494; SERVERID=9ee29c682be9356b7648e0eed94165c1|1728368559|1728368492',
    # 'origin': 'https://weiban.mycourse.cn',
    # 'priority': 'u=1, i',
    # 'referer': 'https://weiban.mycourse.cn/',
    # 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin'
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}
# session = requests.session()
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/nei',methods=['get'])
def nei():
    return render_template("nei.html")


@app.route("/Shu", methods=['POST'])
def Shu():
    json_a = request.get_data()
    json_a = json.loads(json_a)
    School = json_a['School']
    user_name = json_a['user_name']
    user_mm = json_a['user_mm']
    yzm = json_a['yzm']
    now = json_a['now']
    data = {}
    try:

        def get_School():
            ti = time.time()
            url = f'https://weiban.mycourse.cn/pharos/login/getTenantListWithLetter.do?timestamp={ti * 100000}'

            res = requests.post(url, headers=headers).content.decode()
            res = json.loads(res)
            dit = {}
            for i in res['data']:
                for j in i['list']:
                    dit[j['name']] = j['code']
            return dit

        tenantCode = get_School()[School]
        palod = {
            "userName": user_name,
            "password": user_mm,
            "tenantCode": tenantCode,
            "timestamp": now,
            "verificationCode": yzm
        }
        a = JiaM.login(palod)
        # session = requests.session()
        ti = time.time()
        url = f'https://weiban.mycourse.cn/pharos/login/login.do?timestamp={ti * 100000}'
        dat = {
            'data': a
        }
        res = requests.post(url, data=dat).content.decode()
        res = json.loads(res)
        data['data'] = res
        data['state'] = '1'
        data['payload'] = a
        print(res)
    except Exception as e:
        data['state'] = '-1'
        data['data'] = str(e)
    # user_xx = jsonify(data)
    print(data)
    return jsonify(data)

@app.route("/Kai",methods=['POST'])
def Kai():
    json_a = request.get_data()
    json_a = json.loads(json_a)
    print(json_a)
    json_a['data'] = json.loads(json_a['data'])
    userId = json_a['data']['userId']
    token = json_a['data']['token']
    tenantCode = json_a['data']['tenantCode']
    print("名字",json_a['data']['realName'])
    print('学校',json_a['data']['tenantName'])
    print(userId)
    data = {}
    try:
        class Ke:
            def __init__(self):
                self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/?authSource={}'.format("","","","27017",""))['']
            def kai(self):
                # 获取学习中心任务
                ti = time.time()
                new_ti = format(ti,'.3f')
                # print(new_ti)
                url = f'https://weiban.mycourse.cn/pharos/index/listMyProject.do?timestamp={new_ti}'
                headers['x-token'] = token
                print(headers)
                data = {
                    "tenantCode": str(tenantCode),
                    "userId": userId,
                    "ended": "2"
                }
                # print(data)
                res = requests.post(url,data=data,headers=headers).content.decode()
                res = json.loads(res)
                # print(res)
                userProject_id = []
                for i in res['data']:
                    print("课程名字:",i['projectName'])
                    print('结束时间:',i['endTime'])
                    userProject_id.append(i['userProjectId'])
                #获取课程列表
                for i in userProject_id:
                    clas_ti = time.time()
                    new_clasti = format(clas_ti, '.3f')
                    clas_url = f"https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp={new_clasti}"
                    clas_data = {
                        'tenantCode': tenantCode,
                        'userId':userId,
                        'userProjectId': i,
                        'chooseType': '3'
                    }
                    clas_res = requests.post(clas_url,data=clas_data,headers=headers).content.decode()
                    clas_res = json.loads(clas_res)['data']
                    #未完成课的列表
                    categoryCode_dit = {}
                    for j in clas_res:
                        categoryCode_dit[j['categoryCode']] = j['categoryName']
                    # print(categoryCode_dit)
                    for categoryCode,value in categoryCode_dit.items():
                        print(categoryCode,value)
                        xiCla_ti = time.time()
                        now_xiCla = format(xiCla_ti,'.3f')
                        xiCla_url = f'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp={now_xiCla}'
                        data = {
                            'tenantCode': tenantCode,
                            'userId': userId,
                            'userProjectId': i,
                            'chooseType': '3',
                            'categoryCode': categoryCode
                        }
                        xiCla_res = requests.post(xiCla_url,data=data,headers=headers).content.decode()
                        xiCla_res = json.loads(xiCla_res)['data']
                        for Courseid_lis in xiCla_res:
                            if Courseid_lis['finished'] != 2:
                                continue
                            courseId_ti = time.time()
                            now_CourseTi = format(courseId_ti, '.3f')
                            course_url = f"https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp={now_CourseTi}"
                            # print(course_url)
                            course_data = {
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'courseId': Courseid_lis['resourceId'],
                                'userProjectId': i
                            }
                            course_res = requests.post(course_url, headers=headers, data=course_data).content.decode()
                            course_res = json.loads(course_res)

                            userCourseId = course_res['data']
                            # print(userCourseId)
                            userCourseId =  userCourseId.split('?')[1].split('&')[0].split('=')[1]
                            print("userCourseId",userCourseId)
                            #开始学习
                            kai_ti = time.time()
                            now_Kaiti = format(kai_ti,'.3f')
                            kai_url = f"https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={now_Kaiti}"
                            kai_data = {
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'courseId': Courseid_lis['resourceId'],
                                'userProjectId':i
                            }
                            kai_res = requests.post(kai_url,data=kai_data,headers=headers).content.decode()

                            for p in range(15):
                                print("❤",end="")
                                time.sleep(1)
                            print()
                            #获取methonToken
                            url = "https://weiban.mycourse.cn/pharos/usercourse/getCaptcha.do"
                            params = {
                                "userCourseId": userCourseId,
                                "userProjectId": i,
                                "userId":userId,
                                "tenantCode":tenantCode
                            }
                            # print(params)
                            text = requests.get(url, headers=headers, params=params).text
                            # print(text)
                            question_id = json.loads(text)['captcha']['questionId']

                            url = "https://weiban.mycourse.cn/pharos/usercourse/checkCaptcha.do"
                            params = {
                                "userCourseId": userCourseId,
                                "userProjectId": i,
                                "userId": userId,
                                "tenantCode": tenantCode,
                                "questionId": question_id
                            }
                            data = {
                                "coordinateXYs": "[{\"x\":199,\"y\":448},{\"x\":241,\"y\":466},{\"x\":144,\"y\":429}]"
                            }
                            text = requests.post(url, headers=headers, params=params, data=data).text
                            methonToken = json.loads(text)['data']['methodToken']

                            finsh_ti = time.time()
                            now_finshT = format(finsh_ti,'.3f')
                            ts = int(time.time())
                            random_number_string = ''.join(str(random.randint(0, 9)) for _ in range(19))
                            finsh_url = f'https://weiban.mycourse.cn/pharos/usercourse/v2/{methonToken}.do?callback=jQuery{random_number_string}_{ts}&userCourseId={userCourseId}&tenantCode={tenantCode}&_={str(int(ts) + 1)}'
                            text = requests.get(finsh_url, headers=headers).text
                            print("完成",text)
                            time.sleep(3)
                    while True:
                        now = format(time.time(),'.3f')
                        exam_url = f'https://weiban.mycourse.cn/pharos/exam/listPlan.do?timestamp={now}'
                        exam_data = {
                            'tenantCode': tenantCode,
                            'userId': userId,
                            'userProjectId': i
                        }
                        time.sleep(5)
                        exam_res = requests.post(exam_url,headers=headers,data=exam_data).content.decode()
                        print("这是测试数据",exam_res)
                        exam_res = json.loads(exam_res)['data'][0]
                        examPlanId = exam_res['examPlanId']
                        checkVerifyCode_id = exam_res['id']
                        print(checkVerifyCode_id)
                        # print(exam_res)
                        time.sleep(2)
                        yzm_ti = int(time.time() * 1000)
                        yzm_url = f'https://weiban.mycourse.cn/pharos/login/randLetterImage.do?time={yzm_ti}'
                        yzm_res = requests.get(yzm_url,headers=headers).content
                        current_path = os.getcwd()
                        al_path = current_path + '\\' + "image.png"
                        print(al_path)
                        with open('image.png','wb') as f:
                            f.write(yzm_res)
                        while True:
                            if os.path.exists(al_path):
                                break
                            time.sleep(2)
                        ocr = ddddocr.DdddOcr()
                        with open('image.png', 'rb') as f:
                            img_bytes = f.read()
                        res = ocr.classification(img_bytes)

                        #before
                        print(requests.post(f"https://weiban.mycourse.cn/pharos/exam/beforePaper.do?timestamp={format(time.time(), '.3f')}",data={
                            "tenantCode": 65000003,
                            "userId": userId,
                            "userExamPlanId":checkVerifyCode_id
                        },headers=headers).text)


                        #prerper
                        print(requests.post(
                            f"https://weiban.mycourse.cn/pharos/exam/preparePaper.do?timestamp={format(time.time(), '.3f')}",
                            data={
                                "tenantCode": 65000003,
                                "userId": userId,
                                "userExamPlanId": checkVerifyCode_id
                            }, headers=headers).text)




                        checkVerifyCode_ti = format(time.time(),'.3f')
                        checkVerifyCode_url = f'https://weiban.mycourse.cn/pharos/exam/checkVerifyCode.do?timestamp={checkVerifyCode_ti}'
                        checkVerifyCode_data = {
                            'tenantCode': tenantCode,
                            'userId': userId,
                            'time':yzm_ti,
                            'userExamPlanId':checkVerifyCode_id,
                            'verifyCode': res
                        }
                        checkVerifyCode_res = requests.post(checkVerifyCode_url,headers=headers,data=checkVerifyCode_data).content.decode()
                        checkVerifyCode_res = json.loads(checkVerifyCode_res)
                        # print(checkVerifyCode_res)
                        if checkVerifyCode_res['code'] != '0':
                            print("识别错误")
                            continue
                        else:
                            print('识别成功')

                            start_ti = format(time.time(),'.3f')
                            #开始考试
                            start_KaoUrl = f'https://weiban.mycourse.cn/pharos/exam/startPaper.do?timestamp={start_ti}'
                            print("这是考试的链接:",start_KaoUrl)
                            start_data = {
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'userExamPlanId': checkVerifyCode_id
                            }
                            print("这是data:",start_data)
                            start_res = requests.post(start_KaoUrl,headers=headers,data=start_data).content.decode()
                            print("开始res",start_res)


                            start_res = json.loads(start_res)['data']['questionList']
                            cuo_num = 0
                            print("爬取问题")
                            time.sleep(5)
                            dui_num = 0
                            for i in start_res:
                                title = i['title']
                                arr = self.client['z_ti'].find_one({'title':title})
                                if arr != None:
                                    do_ti = format(time.time(), '.3f')
                                    do_url = f'https://weiban.mycourse.cn/pharos/exam/recordQuestion.do?timestamp={do_ti}'
                                    anser_lis = []
                                    for j in i['optionList']:
                                        if j['content'] in arr['optionList']:
                                            anser_lis.append(j['id'])
                                    do_data = {
                                        'tenantCode': tenantCode,
                                        'userId': userId,
                                        'userExamPlanId': checkVerifyCode_id,
                                        'questionId': i['id'],
                                        'useTime': random.randint(1, 100),
                                        'answerIds': ','.join(anser_lis),
                                        'examPlanId': examPlanId,
                                    }
                                    # print(do_data)
                                    do_res = requests.post(do_url, headers=headers, data=do_data).content.decode()
                                    dui_num += 1
                                    print(do_res,"对的",f'对了 {dui_num}')
                                    time.sleep(1)
                                else:
                                    cuo_num += 1
                                    print(f"错{cuo_num}")
                                    do_ti = format(time.time(), '.3f')
                                    do_url = f'https://weiban.mycourse.cn/pharos/exam/recordQuestion.do?timestamp={do_ti}'
                                    anser_lis = []
                                    for j in i['optionList']:
                                        anser_lis.append(j['id'])
                                        break
                                    do_data = {
                                        'tenantCode': tenantCode,
                                        'userId': userId,
                                        'userExamPlanId': checkVerifyCode_id,
                                        'questionId': i['id'],
                                        'useTime': random.randint(1, 100),
                                        'answerIds': ','.join(anser_lis),
                                        'examPlanId': examPlanId,
                                    }
                                    # print(do_data)
                                    do_res = requests.post(do_url, headers=headers, data=do_data).content.decode()
                            print(f"有{cuo_num}题不确定答案")

                            sub_params = {
                                'timestamp': format(time.time(),'.3f'),
                            }
                            sub_data = {
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'userExamPlanId': checkVerifyCode_id,
                            }

                            sub_res = requests.post('https://weiban.mycourse.cn/pharos/exam/submitPaper.do',params=sub_params,headers=headers,data=sub_data).content.decode()
                            sub_res = json.loads(sub_res)['data']['score']
                            print(f"{sub_res}分")
                            time.sleep(2)


                            get_tiTi = format(time.time(),'.3f')
                            get_tiUrl = f'https://weiban.mycourse.cn/pharos/exam/listHistory.do?timestamp={get_tiTi}'
                            get_data={
                                'tenantCode': tenantCode,
                                'userId': userId,
                                'examPlanId':examPlanId,
                                'examType': '2',
                            }
                            get_res = requests.post(get_tiUrl,headers=headers,data=get_data).content.decode()

                            get_res = json.loads(get_res)['data']
                            grade_lis = []
                            for grade in get_res:
                                grade_lis.append(grade['id'])
                            for ti in grade_lis:
                                ti_url = f'https://weiban.mycourse.cn/pharos/exam/reviewPaper.do?timestamp={format(time.time(),".3f")}'
                                ti_data = {
                                    'tenantCode': tenantCode,
                                    'userId': userId,
                                    'userExamId': ti,
                                    'isRetake': '2',
                                }
                                ti_res = requests.post(ti_url,headers=headers,data=ti_data).content.decode()
                                ti_res = json.loads(ti_res)['data']['questions']
                                num = 0
                                for i in ti_res:
                                    arr = self.client["z_ti"].find_one({"title": i['title']})
                                    lis = []
                                    if arr == None:
                                        for j in i['optionList']:
                                            if j['isCorrect'] == 1 or j['isCorrect'] == '1':
                                                lis.append(j['content'])
                                        self.client["z_ti"].insert_one({'title': i['title'], "optionList": lis})
                                        num += 1
                                print(f"有{num}题没有")
                                time.sleep(2)
                                url = f'https://weiban.mycourse.cn/pharos/my/getInfo.do?timestamp={format(time.time(),".3f")}'
                                data = {
                                    'tenantCode': tenantCode,
                                    'userId': userId
                                }
                                res = requests.post(url, data=data, headers=headers).content.decode()

                                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                j_res = json.loads(res)['data']
                                flag = self.client['user'].count_documents({'id': j_res['studentNumber']})
                                if flag == 1:
                                    self.client['user'].update_one({'id': j_res['studentNumber']},{ "$set": { "ti": t } })
                                else:
                                    self.client['user'].insert_one({'nianJi': j_res['batchName'], 'sexy': j_res['gender'],
                                                       'xueyuan': j_res['orgName'], 'id': j_res['studentNumber'],
                                                       'realName': j_res['realName'], 'zy': j_res['specialtyName'],
                                                       'ti': t})
        k = Ke()
        k.kai()
        data['data'] = '1'
    except Exception as e:
        data['data'] = str(e)
    return jsonify(data)










if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)