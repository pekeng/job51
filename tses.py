import requests
import re
import execjs
from lxml import etree
from chaojiying import Chaojiying_Client
from parse_image import get_new_image


def get_js2():
    f = open("getguid.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def parse_giud():
    jsstr = get_js2()
    ctx = execjs.compile(jsstr)  # 加载JS文件
    return ctx.call('eee') # 调用js方法  第一个参数是JS的方法名，后面的data是js方法的参数


def parse_tk(n1, o1):
    jsstr = get_js2()
    ctx = execjs.compile(jsstr)  # 加载JS文件
    return ctx.call('sss', n1, o1)  # 调用js方法  第一个参数是JS的方法名，后面的data是js方法的参数


def job51(vip_name, user_name, user_password,dama_user_name,dama_password,dama_id):
    headers = {
        "Accept": "*/*;",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Host": "ehire.51job.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    headers1 = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://ehire.51job.com/MainLogin.aspx",
        "Origin": "https://ehire.51job.com",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Host": "ehirelogin.51job.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    session = requests.session()
    res1 = session.get(url="https://ehire.51job.com/MainLogin.aspx", headers=headers, verify=False)
    response = etree.HTML(res1.text)
    view_start = "".join(response.xpath('//*[@id="__VIEWSTATE"]/@value')).strip()
    hidlangtype = "".join(response.xpath('//*[@id="hidLangType"]/@value')).strip()
    hidaccesskey = "".join(response.xpath('//*[@id="hidAccessKey"]/@value')).strip()
    fksc = "".join(response.xpath('//*[@id="fksc"]/@value')).strip()
    hidehireguid = "".join(response.xpath('//*[@id="hidEhireGuid"]/@value')).strip()
    hidtkey = "".join(response.xpath('//*[@id="hidTkey"]/@value')).strip()
    key = re.findall(r" AccessKey=(.*?);", str(res1.headers))[0].strip()
    data11 = {
        "d": "gt",
        "key": "".format(fksc)
    }
    res11 = session.post(
        url="https://ehire.51job.com/ajax/Sec/v.aspx",
        data=data11,
        headers=headers, verify=False)
    # 解决tk与giud
    n1 = re.findall(r's="(.*?)"', res11.text)[0]
    o1 = re.findall(r'p="(.*?)"', res11.text)[0]
    tk = parse_tk(n1=n1, o1=o1)
    giud = parse_giud()
    session.cookies.pop("ASP.NET_SessionId")
    # 请求图片
    headers.update(
        {"Accept": "*/*", "Referer": "https://ehire.51job.com/MainLogin.aspx", "Origin": "https://ehire.51job.com"})
    res2 = session.get(
        url="https://ehire.51job.com/ajax/Validate/LoginValidate.aspx?doType=getverify&key={}&guid={}".format(key,giud),
        headers=headers, verify=False)
    with open('full.jpg', 'wb') as f:
        f.write(res2.content)
        print('full.jpg生成成功')
    # 合成图片
    get_new_image()
    print("图片合成成功！！")
    # 图片识别超级鹰打码平台
    chaojiying = Chaojiying_Client(dama_user_name, dama_password, dama_id)
    image = open('image1.jpg', 'rb').read()  
    chaojiying_response = chaojiying.PostPic(image, 9104)  # 9104 验证码类型  
    p = re.findall(r"'pic_str': '(.*?)',", str(chaojiying_response))
    if p and "OK" in str(chaojiying_response):
        print("打码成功！！")
        p = p[0].replace("|", ";")
        p = p.replace(",", " ").replace(";", " ").split()
        p = p[0] + "," + str(int(p[1]) - 50) + ";" + p[2] + "," + str(int(p[3]) - 50) + ";" + p[4] + "," + str(
            int(p[5]) - 50) + ";" + p[6] + "," + str(int(p[7]) - 50)
        data2 = {"dotype": "checkverift",
                 "key": key,
                 "p": p,
                 "guid": giud}
        yanzhen_response = session.post(
            url="https://ehire.51job.com/ajax/Validate/LoginValidate.aspx",
            headers=headers,
            data=data2,
            verify=False)
        # 如果result不为0则为注册key,giud成功,因为后面登陆login_data主要验证这俩参数
        print(yanzhen_response.text)
        session.get(url="https://ehire.51job.com/MainLogin.aspx", headers=headers, verify=False)
        login_data = {"__VIEWSTATE": view_start,
                      "hidRetUrl": "",
                      "hidLangType": hidlangtype,
                      "hidAccessKey": hidaccesskey,
                      "fksc": fksc,
                      "hidEhireGuid": hidehireguid,
                      "hidTkey": hidtkey,
                      "hidVGuid": giud,
                      "txtMemberNameCN": vip_name,
                      "txtUserNameCN": user_name,
                      "txtPasswordCN": user_password,
                      "ctmName": vip_name,
                      "userName": user_name,
                      "password": user_password,
                      "checkCode": "",
                      "oldAccessKey": hidaccesskey,
                      "langtype": hidlangtype,
                      "isRememberMe": "false",
                      "sc": fksc,
                      "ec": hidehireguid,
                      "returl": "",
                      "referrurl": "https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N",
                      "tk": tk,
                      "sk": hidtkey,
                      "verifyGuid": giud
                      }
        print("登陆所需data{}".format(login_data))
        # 开始登陆
        res3 = session.post(url="https://ehirelogin.51job.com/Member/UserLogin.aspx?",
                            headers=headers1,
                            data=login_data,
                            verify=False,
                            )
        if user_name in str(res3.text):
            if "强制下线" not in str(res3.text):
                print("用户{}登陆成功！！".format(user_name))
                # 进入已下载简历的页面第一页
                start_page_url = "https://ehire.51job.com/InboxResume/CompanyHRDefault2.aspx?Page=2&belong=3"
                headers.update({"Referer": "https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
                headers.pop("Origin")
                # session对话不能保存请求cookie？
                cookies2 = requests.utils.dict_from_cookiejar(session.cookies)
                session.cookies.update(cookies2)
                first_page_response = session.get(
                    url=start_page_url,
                    headers=headers,
                    verify=False,
                )
                first_page_response = etree.HTML(first_page_response.text)
                viewstart1 = "".join(first_page_response.xpath('//*[@id="__VIEWSTATE"]/@value')).strip()
                hidcheckuserids1 = "".join(first_page_response.xpath('//*[@id="hidCheckUserIds"]/@value')).strip()
                hidcheckkey1 = "".join(first_page_response.xpath('//*[@id="hidCheckKey"]/@value')).strip()
                hidaccesskey1 = "".join(first_page_response.xpath('//*[@id="hidAccessKey"]/@value')).strip()
                all_url_list = []
                while hidcheckuserids1:
                    # 请求下一页实现增量爬取
                    next_data = {
                        "__EVENTTARGET": "pagerBottomNew$nextButton",
                        "__VIEWSTATE": viewstart1,
                        "CandidateFolder$hid_keywordtype": "1",
                        "CandidateFolder$hidShowMore": "0",
                        "CandidateFolder$hidmorelistheight": "126",
                        "txt_posttime": "近3个月",
                        "hid_posttime": "90",
                        "pagerTopNew$ctl06": "10",
                        "cbxColumns$0": "AGE",
                        "cbxColumns$1": "WORKYEAR",
                        "cbxColumns$2": "SEX",
                        "cbxColumns$3": "AREA",
                        "cbxColumns$4": "TOPDEGREE",
                        "cbxColumns$13": "SOURCE",
                        "cbxColumns$14": "JOBNAME",
                        "cbxColumns$16": "PUTDATE",
                        "exportType": "Word",
                        "downloadType": "0",
                        "screen": "0",
                        "rdbCustomize": "on",
                        "chk_intvplan": "on",
                        "intvresult": "1",
                        "chk_offerplan": "on",
                        "offerresult": "1",
                        "hidPageFlag": "0",
                        "hidFolder": "BAK",
                        "hidDisplayType": "0",
                        "hidCheckUserIds": hidcheckuserids1,
                        "hidCheckKey": hidcheckkey1,
                        "hidSort": "PUTDATE",
                        "hidShowCode": "0",
                        "hidAccessKey": hidaccesskey1
                    }
                    next_url = "https://ehire.51job.com/InboxResume/CompanyHRDefault2.aspx?Page=2&belong=3"
                    next_page_response = session.post(
                        url=next_url,
                        headers=headers,
                        data=next_data,
                        verify=False,
                    )
                    next_page_response = etree.HTML(next_page_response.text)
                    viewstart1 = "".join(next_page_response.xpath('//*[@id="__VIEWSTATE"]/@value')).strip()
                    hidcheckuserids1 = "".join(
                        next_page_response.xpath('//*[@id="hidCheckUserIds"]/@value')).strip()
                    hidcheckkey1 = "".join(next_page_response.xpath('//*[@id="hidCheckKey"]/@value')).strip()
                    hidaccesskey1 = "".join(next_page_response.xpath('//*[@id="hidAccessKey"]/@value')).strip()
                    # 下一页失效
                    mark = "".join(next_page_response.xpath('//*[@id="pagerBottomNew_nextButton"]/@class')).strip()
                    for i in range(1, 11):
                        one_url = "".join(next_page_response.xpath(
                            '//*[@id="trBaseInfo_{}"]/td[3]/ul/li[1]/a/@href'.format(i))).strip()
                        if one_url:
                            if "https" in one_url:
                                all_url_list.append(one_url)
                            else:
                                all_url_list.append("https://ehire.51job.com" + one_url)
                    # 死循环停止条件
                    if "aspNetDisabled" in mark:
                        hidcheckuserids1 = None
                # 请求每一个人的简历
                if all_url_list:
                    print(all_url_list)
                    # url去重
                    all_url_list = list(set(all_url_list))
                    headers.pop("Referer")
                    for user_url in all_url_list:
                        if user_url:
                            user_url = user_url.strip()
                            user_resume_response = session.get(url=user_url, headers=headers, verify=False, )
                            if user_resume_response.status_code == 200:
                                user_resume_response = etree.HTML(user_resume_response.text)
                                try:
                                    update_time = "".join(user_resume_response.xpath(
                                        '//*[@id="lblResumeUpdateTime"]/text()')).strip().replace(" ", "")
                                    seek_name = "".join(user_resume_response.xpath(
                                        '//*[@id="tdseekname"]/text()')).strip().replace(" ", "")
                                    tag = "".join(user_resume_response.xpath(
                                        '//td[@colspan="3"]/table/tr/td/text()[2]')).strip().replace(" ", "")  #
                                    telephone = "".join(user_resume_response.xpath(
                                        '//td[@colspan="3"]/table/tr/td[2]/text()')).strip().replace(" ", "")  #
                                    mail = "".join(user_resume_response.xpath(
                                        '//td[@class="m_com"]/a[@class="blue"]/text()')).strip().replace(" ", "")
                                    gender = "".join(user_resume_response.xpath(
                                        '//tr/td[@colspan="3"]/text()[2]')).strip().replace(" ", "")
                                    age_birthday = "".join(user_resume_response.xpath(
                                        '//tr/td[@colspan="3"]/text()[3]')).strip().replace(" ", "")
                                    now_address = "".join(user_resume_response.xpath(
                                        '//tr/td[@colspan="3"]/text()[4]')).strip().replace(" ", "")
                                    work_experience = "".join(user_resume_response.xpath(
                                        '//tr/td[@colspan="3"]/text()[5]')).strip().replace(" ", "")
                                    print("这是解析之后的数据时间：{}电话：{}".format(mail, telephone))
                                    print(update_time, seek_name, tag, telephone, mail, gender, age_birthday,
                                          now_address, work_experience)
                                    recent_work_time = "".join(user_resume_response.xpath(
                                        '//td[@class="plate2"]/span[@class="normal"]/text()')).strip()
                                    position = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[2]/td[@class="txt2"]/text()')[0]).strip()
                                    professional = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[2]/td[@class="txt2"]/text()')[-1]).strip()
                                    company = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[3]/td[@class="txt2"]/text()')[0]).strip()
                                    school = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[3]/td[@class="txt2"]/text()')[-1]).strip()
                                    industry = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[4]/td[@class="txt2"]/text()')[0]).strip()
                                    edu_background = "".join(user_resume_response.xpath(
                                        '//table/tbody/tr[4]/td[@class="txt2"]/text()')[-1]).strip()
                                    print("最近工作!!!{}")
                                    print(recent_work_time, position, professional, company, school,
                                          industry, edu_background, )
                                    # 个人信息
                                    nationality = "".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr/td[2]/text()')).strip()
                                    mari_status = "".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/text()')).strip()
                                    home_address = "".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[1]/table/tbody/tr/td[2]/text()')).strip()
                                    political_status = "".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[1]/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[2]/text()')).strip()

                                    # 目前收入
                                    now_income = "".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[2]/tbody/tr[1]/td/span[@class="f16"]/text()')).strip()
                                    print(nationality,mari_status,home_address,political_status)
                                    if now_income:
                                        # 求职意向
                                        job_intention="".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[3]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td/text()')).strip()
                                        # 工作经验
                                        work_experience_detail="".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[4]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/text()')).strip()
                                        # 项目经验
                                        project_experience="".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[5]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr\
                                        /td/text()|\//*[@id="divInfo"]/td/table[5]/tbody/tr/td/table/tbody/tr/td/table\
                                        /tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[5]/tbody/tr[2]/td/table\
                                        /tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/text()')).strip()
                                        #教育经历
                                        edu_experience="".join(user_resume_response.xpath(
                                        '//*[@id="divInfo"]/td/table[last()-3]/tbody/tr[2]/td/table/tbody/tr/td/table\
                                        /tbody/tr/td/text()|//*[@id="divInfo"]/td/table[last()-3]/tbody/tr[2]/td/table\
                                        /tbody/tr/td/table/tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[last()-2]\
                                        /tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody\
                                        /tr/td/text()')).strip()
                                        if edu_experience:
                                            pass
                                        else:
                                            edu_experience = "".join(user_resume_response.xpath(
                                                '//*[@id="divInfo"]/td/table[last()-2]/tbody/tr[2]/td/table/tbody/tr/td/table\
                                                /tbody/tr/td/text()|//*[@id="divInfo"]/td/table[last()-2]/tbody/tr[2]/td/table\
                                                /tbody/tr/td/table/tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[last()-2]\
                                                /tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody\
                                                /tr/td/text()')).strip()
                                        # 技能特长
                                        skills="".join(user_resume_response.xpath(
                                            '//td[@class="skill"]/strong/text()|//td[@valign="top"]/span[@class="skbg"]/span/text()\
                                            |//*[@id="divInfo"]/td/table[7]/tbody/tr[2]/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/text()')).strip()
                                    else:
                                        # 求职意向
                                        job_intention_json = "".join(user_resume_response.xpath(
                                            '//*[@id="divInfo"]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td/text()')).strip()
                                        # 工作经验
                                        work_experience_detail = "".join(user_resume_response.xpath(
                                            '//*[@id="divInfo"]/td/table[3]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/text()')).strip()
                                        # 项目经验
                                        project_experience = "".join(user_resume_response.xpath(
                                            '//*[@id="divInfo"]/td/table[4]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr\
                                            /td/text()|\//*[@id="divInfo"]/td/table[4]/tbody/tr/td/table/tbody/tr/td/table\
                                            /tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[4]/tbody/tr[2]/td/table\
                                            /tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/text()')).strip()
                                        # 教育经历
                                        edu_experience = "".join(user_resume_response.xpath(
                                            '//*[@id="divInfo"]/td/table[last()-3]/tbody/tr[2]/td/table/tbody/tr/td/table\
                                            /tbody/tr/td/text()|//*[@id="divInfo"]/td/table[last()-3]/tbody/tr[2]/td/table\
                                            /tbody/tr/td/table/tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[last()-2]\
                                            /tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody\
                                            /tr/td/text()')).strip()
                                        if edu_experience:
                                            pass
                                        else:
                                            edu_experience = "".join(user_resume_response.xpath(
                                                '//*[@id="divInfo"]/td/table[last()-2]/tbody/tr[2]/td/table/tbody/tr/td/table\
                                                /tbody/tr/td/text()|//*[@id="divInfo"]/td/table[last()-2]/tbody/tr[2]/td/table\
                                                /tbody/tr/td/table/tbody/tr/td/strong/text()|//*[@id="divInfo"]/td/table[last()-2]\
                                                /tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody\
                                                /tr/td/text()')).strip()
                                            # 技能特长
                                            skills = "".join(user_resume_response.xpath(
                                                '//*[@id="divInfo"]/td/table[8]/tbody/tr[2]/td/table/tbody/tr/td/text()\
                                                |//*[@id="divInfo"]/td/table[8]/tbody/tr[2]/td/table/tbody/tr[2]/td/table\
                                                /tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/strong/text()|')).strip()
                                except Exception as e:
                                    print("请求简历出错{}".format(e))
            else:
                print("请在浏览器上强制先下线再登陆！！")
        else:
            print("用户{}登陆失败！请检查账号密码是否错误！".format(user_name))
    else:
        print("打码平台错误{}!请检查充值！".format(chaojiying_response))


if __name__ == '__main__':
    job51(vip_name="", user_name="", user_password="",
          dama_user_name="",dama_password="",dama_id="") # 用户中心>>软件ID 生成一个替换 96001
