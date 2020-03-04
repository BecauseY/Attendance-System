from flask import Flask,render_template,request,session,redirect,url_for
import os
import pymysql
import time
import PunchVerification
import json
from datetime import timedelta
import datetime
import base64
import face_identify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 设置session的保存时间。


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/check', methods=['post', 'get'])
def check():
    datas = request.get_json(force=True)
    data = datas["data2"]
    imgdata = base64.b64decode(data)

    name_id = session.get('name_id')
    rva = '.\\static\\face\\'
    pic_format = '.jpg'
    addr_photo = rva + name_id + pic_format
    print(addr_photo)
    file = open(addr_photo, 'wb')
    file.write(imgdata)
    file.close()

    name_id = session.get('name_id')
    re = face_identify.face_identify(name_id)
    print(re)
    if(re):
        result = "yes"
    else:
        result = 'no'
    status={"yesorno": result}
    return json.dumps(status)
    # return render_template("index.html")

@app.route('/main/statistic')
def statistic():
    nameid = session.get('name_id')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `name`, `date`, `sign_in_time`, `sign_out_time` FROM `sign` WHERE name_id =" + nameid
    cur.execute(sql)
    realp = cur.fetchall()
    conn.close()

    month = []           # 存放打卡记录中的月份数
    dt1 = []             # 二维列表 存放每一条用户名 日期 签到签退时间

    for i in range(len(realp)):
        dt = list(realp[i])
        dt1.insert(i, dt)
        month.insert(i, str(realp[i][1].month))

    n = len(month)      # n存放打卡总天数

    m1 = m2 = m3 = m4 = m5 = m6 = m7 = m8 = m9 = m10 = m11 = m12 = 0         # 存放每个月的打卡次数
    # 月份数据列表
    u1 = []
    u2 = []
    u3 = []
    u4 = []
    u5 = []
    u6 = []
    u7 = []
    u8 = []
    u9 = []
    u10 = []
    u11 = []
    u12 = []
    # 每个月的月份数组 存放签到时间，签退时间，设置时间

    for i in range(n):                             # 记录每个月打卡次数
        if str(month[i]) == '1':
            m1 += 1
        elif str(month[i]) == '2':
            m2 += 1
        elif str(month[i]) == '3':
            m3 += 1
        elif str(month[i]) == '4':
            m4 += 1
        elif str(month[i]) == '5':
            m5 += 1
        elif str(month[i]) == '6':
            m6 += 1
        elif str(month[i]) == '7':
            m7 += 1
        elif str(month[i]) == '8':
            m8 += 1
        elif str(month[i]) == '9':
            m9 += 1
        elif str(month[i]) == '10':
            m10 += 1
        elif str(month[i]) == '11':
            m11 += 1
        elif str(month[i]) == '12':
            m12 += 1

    u = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]              # 记录每个月打卡天数
    u0 = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]             # 存放月份数据列表

    for i in range(12):                          # 将每个月打卡次数存放进月份数组的第一项
        if u[i] != 0:
            u0[i].insert(0, u[i])

    conn1 = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur1 = conn1.cursor()
    sqll = "SELECT `date`,  `sign_in_time`, `sign_out_time` FROM `sign` WHERE name_id =" + nameid
    cur1.execute(sqll)
    u11 = cur1.fetchall()                 # 获得签到信息

    conn0 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur0 = conn0.cursor()
    sqllll = "SELECT * FROM `setting` "
    cur0.execute(sqllll)
    Standard_setting = cur0.fetchall()           # 获得设置信息

    deadline = str(Standard_setting[0][0])
    closing_time = str(Standard_setting[0][1])

    for j in range(12):
        timerecord = []
        for i in range(len(u11)):
            if str(u11[i][0].month) == str(j+1):
                data = [u11[i][1], u11[i][2], deadline, closing_time]
                timerecord.append(data)
        u0[j].append(timerecord)

    monthdata = []            # 存储最终月度签到数据
    for i in range(12):
        if u0[i] != [[]]:
            n1 = n2 = n3 = n4 = 0
            for j in range(len(u0[i][1])):         # 对每个月数据进行统计
                d1 = datetime.datetime.strptime(str(u0[i][1][j][0]), '%H:%M:%S')
                d2 = datetime.datetime.strptime(str(u0[i][1][j][1]), '%H:%M:%S')
                d3 = datetime.datetime.strptime(str(u0[i][1][j][2]), '%H:%M:%S')
                d4 = datetime.datetime.strptime(str(u0[i][1][j][3]), '%H:%M:%S')
                delta1 = d3 - d1
                delta2 = d4 - d2

                if delta1 > datetime.timedelta(0):
                    late = False
                else:
                    late = True

                if delta2 > datetime.timedelta(0):
                    leave_early = True
                else:
                    leave_early = False

                if (late is False) and (leave_early is False):  # 无异常
                    n1 += 1

                elif (late is False) and (leave_early is True):  # 早退
                    n2 += 1

                elif (late is True) and (leave_early is False):  # 迟到
                    n3 += 1

                elif (late is True) and (leave_early is True):  # 早退并迟到
                    n4 += 1
            data_i = [i+1, u0[i][0], n1, n2, n3, n4, '%.2f%%' % (n1/u0[i][0])]
            monthdata.insert(i, data_i)
    conn1.close()
    return render_template('statistic.html', u = monthdata)



@app.route('/main/', methods=['post','get'])
def yanzheng():
    nameid = request.form['login']
    ps = request.form['password']

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `name`, `password` FROM `information` WHERE name_id =" + nameid
    cur.execute(sql)
    realps = cur.fetchall()
    conn.close()

    session.permanent = True  # 默认session的时间持续31天
    session['name_id'] = nameid
    session['name_name'] = realps[0][0]
    if ps == realps[0][1] :
        return render_template('face.html')
    else:
        return render_template('login.html')


@app.route('/message', methods=['post', 'GET'])
def shenqing():
    shenqing_leixing = request.form['leixing']
    shenqing_shijian = request.form['shenqingshijian']
    shenqing_liyou = request.form['shenqingliyou']
    shenqing_name = session.get('name_name')
    shenqing_nameid = session.get('name_id')

    if shenqing_leixing == 'buqian':
        leixing = 'retroactive'
    elif shenqing_leixing == 'qingjia':
        leixing = 'dayoff'
    elif shenqing_leixing == 'chuchai':
        leixing = 'business_trip'

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()
    sql = "INSERT INTO `"+str(leixing)+"`(`name`, `name_id`, `date`, `reason`, `result`) VALUES ('"+str(shenqing_name)+"','"+str(shenqing_nameid)+"','"+str(shenqing_shijian)+"','"+str(shenqing_liyou)+"','未处理');"
    # print(sql)
    cur.execute(sql)
    personmessage = cur.fetchall()
    conn.close()
    print(personmessage)
    res = {'status': 1}

    return render_template('index.html')


@app.route('/sign_in',  methods=['post'])
def sign_in():

    name = session.get('name_name')
    name_id = session.get('name_id')
    date = time.strftime("%Y-%m-%d", time.localtime())
    sign_in_time = time.strftime("%H:%M:%S", time.localtime())

    data = request.get_json(force=True)  # 获取json数据
    CurLongitude= data['jingdu']
    CurLatitude=  data['weidu']
    print(CurLongitude)
    print(CurLatitude)

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()

    sql = "SELECT * FROM `setting` "
    cur.execute(sql)
    Standard_setting = cur.fetchall()
    LocationLongitude = Standard_setting[0][2]
    LocationLatitude = Standard_setting[0][3]
    LocationRadius  = Standard_setting[0][4]

    WhereAreYouSignIn=PunchVerification.WhereAreYou(CurLongitude,CurLatitude,LocationLongitude,LocationLatitude,LocationRadius)

    sql = "SELECT * FROM `sign` WHERE name_id = '"+str(name_id)+"' AND date= '"+date+"';"
    cur.execute(sql)
    sign_in_record_today = str(cur.fetchall())
    if sign_in_record_today != '()':               # if sign in repeatedly
        repeatedly_sign_in = True
    else:
        repeatedly_sign_in = False

    if WhereAreYouSignIn  and not repeatedly_sign_in:  # and not late

        sql = "INSERT INTO sign (name, name_id, date, sign_in_time) VALUES('"+str(name)+"','"+str(name_id)+"','"+str(date)+"','"+str(sign_in_time)+"');"
        print("sign_in sceess")
        print(sql)
        cur.execute(sql)
    else:
        print("sign_in failed")
    conn.close()

    return json.dumps(data)


@app.route('/sign_out',  methods=['post'])
def sign_out():
    name = session.get('name_name')
    name_id = session.get('name_id')
    date = time.strftime("%Y-%m-%d", time.localtime())
    sign_out_time = time.strftime("%H:%M:%S", time.localtime())

    data = request.get_json(force=True)  # 获取json数据
    CurLongitude = data['jingdu']
    CurLatitude = data['weidu']

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()

    sql = "SELECT * FROM `setting` "
    cur.execute(sql)
    Standard_setting = cur.fetchall()
    LocationLongitude = Standard_setting[0][2]
    LocationLatitude = Standard_setting[0][3]
    LocationRadius = Standard_setting[0][4]

    WhereAreYouSignOut = PunchVerification.WhereAreYou(CurLongitude,CurLatitude,LocationLongitude,LocationLatitude,LocationRadius)

    sql = "SELECT * FROM `sign` WHERE name_id = '" + str(name_id) + "' AND date= '" + date + "';"
    # print(sql)
    cur.execute(sql)
    sign_out_record_today = str(cur.fetchall())
    # print(sign_out_record_today)
    if sign_out_record_today != '()':  # if sign in repeatedly
        no_sign_in_record = False        # no
    else:
        no_sign_in_record = True
    # print(WhereAreYouSignOut,no_sign_in_record)

    if WhereAreYouSignOut  and not no_sign_in_record:  # and not leave_early
        sql = "UPDATE `sign` SET sign_out_time = '"+str(sign_out_time)+"' WHERE date = '"+str(date)+"' AND name_id='"+str(name_id)+"';"
        cur.execute(sql)
        conn.close()
    else:
        print("sign_out failed")

    return json.dumps(data)


@app.route('/record', methods=["post","get"])
def record():
    jilu_nameid = session.get('name_id')
    conn0 = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur0 = conn0.cursor()
    sqllll = "SELECT * FROM `setting` "
    cur0.execute(sqllll)
    Standard_setting = cur0.fetchall()
    sqllll = "SELECT * FROM `sign`"
    cur0.execute(sqllll)

    deadline = str(Standard_setting[0][0])
    closing_time = str(Standard_setting[0][1])

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `name`, `password` FROM `information` WHERE name_id =" + jilu_nameid
    cur.execute(sql)
    realps = cur.fetchall()
    conn.close()

    conn1 = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur1 = conn1.cursor()
    sqll = "SELECT `date`,  `sign_in_time`, `sign_out_time` FROM `sign` WHERE name_id =" + jilu_nameid
    cur1.execute(sqll)
    u11 = cur1.fetchall()
    u1 = []

    for i1 in range(len(u11)):
        d1 = datetime.datetime.strptime(str(u11[i1][1]), '%H:%M:%S')
        d2 = datetime.datetime.strptime(str(u11[i1][2]), '%H:%M:%S')
        d3 = datetime.datetime.strptime(deadline, '%H:%M:%S')
        d4 = datetime.datetime.strptime(closing_time, '%H:%M:%S')
        delta1 = d3 - d1
        delta2 = d4 - d2

        if delta1 > datetime.timedelta(0):
            late = False
        else:
            late = True

        if delta2 > datetime.timedelta(0):
            leave_early = True
        else:
            leave_early = False

        if (late is False) and (leave_early is False):  # 无异常
            list1 = list(u11[i1])
            list1.insert(3, '正常')
            u1.insert(i1, list1)

        elif (late is False) and (leave_early is True):  # 早退
            list1 = list(u11[i1])
            default = '1900-01-01 00:00:00'
            if (str(d2) == default) is False:
                list1.insert(3, '早退')
            else:
                list1.insert(3, '未签退')
            u1.insert(i1, list1)

        elif (late is True) and (leave_early is False):  # 迟到
            list1 = list(u11[i1])
            list1.insert(3, '迟到')
            u1.insert(i1, list1)

        elif (late is True) and (leave_early is True):  # 早退并迟到
            list1 = list(u11[i1])
            default = '1900-01-01 00:00:00'
            if (str(d2) == default) is False:
                list1.insert(3, '迟到并早退')
            else:
                list1.insert(3, '迟到 未签退')
            u1.insert(i1, list1)
    conn1.close()
    print(u1)
    for i in range(len(u1)):
        u1[i][0] = str(u1[i][0])
        u1[i][1] = str(u1[i][1])
        u1[i][2] = str(u1[i][2])
    return json.dumps(u1)


@app.route('/xiaoxi', methods=['post', 'get'])
def xiaoxi():
    xiaoxi_nameid = session.get('name_id')
    conn2 = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur2 = conn2.cursor()
    sqlll = "SELECT  `date`, `reason`, `result` FROM `retroactive` WHERE name_id =" + xiaoxi_nameid
    cur2.execute(sqlll)
    u21 = cur2.fetchall()
    u2 = []

    for i in range(len(u21)):
        list1 = list(u21[i])
        list1.insert(3, '补签')
        u2.insert(i, list1)

    conn2.close()

    conn3 = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur3 = conn3.cursor()
    sqlll = "SELECT `date`, `reason`, `result` FROM `dayoff` WHERE name_id =" + xiaoxi_nameid
    cur3.execute(sqlll)
    u31 = cur3.fetchall()
    u3 = []

    for i in range(len(u31)):
        list2 = list(u31[i])
        list2.insert(3, '请假')
        u3.insert(i, list2)

    conn3.close()

    conn4 = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur4 = conn4.cursor()
    sqlll = "SELECT `date`, `reason`, `result` FROM `business_trip` WHERE name_id =" + xiaoxi_nameid
    cur4.execute(sqlll)
    u41 = cur4.fetchall()
    u4 = []

    for i in range(len(u41)):
        list3 = list(u41[i])
        list3.insert(3, '出差')
        u4.insert(i, list3)

    conn4.close()

    u2 = u2 + u3 + u4
    for i in range(len(u2)):
        u2[i][0] = str(u2[i][0])

    return json.dumps(u2)





@app.route('/admin')
def adminindex():
   return render_template('main.html')

#|------------------------------------set_signin------------------------------------|
@app.route('/admin/set_signin')
def setsign():
   return render_template('set_signin.html')

@app.route('/admin/set_sign', methods=['POST','GET'])
def set_signin():
    print(1)
    sign_in_time = request.form.get('go')
    sign_out_time = request.form.get('leave')
    longitude = request.form.get('position1')
    latitude = request.form.get('position2')
    range = request.form.get('distance')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='ci', charset='utf8')
    cursor = conn.cursor()
    sql = 'DELETE FROM setting'
    cursor.execute(sql)
    sql = "INSERT INTO setting VALUES ('%s','%s','%s','%s','%s')" % (sign_in_time,sign_out_time,longitude,latitude,range)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close
    conn.close()
    return render_template('set_signin.html')


# |------------------------------------checksignin------------------------------------|
@app.route('/admin/checksignin/', methods=['POST','GET'])
def check_signin():
    if request.method == 'POST':
        date_to_find = request.form.get('date')
        print(date_to_find)

        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()

        sql1 = "SELECT * FROM sign"
        cur.execute(sql1)
        u1 = cur.fetchall()

        sql2 = "SELECT sign_in_time,sign_out_time FROM setting"
        cur.execute(sql2)
        u2 = cur.fetchall()


        # 遍历当天所有name_id的签到信息，若未在sign表中找到该name_id，在查询business表和dayoff表，合并单元格为“未签到”/“出差”/“请假”
        sql3 = "SELECT name_id FROM information"  # 从information表中先找到所有的name_id
        cur.execute(sql3)
        u3 = cur.fetchall()
        print(u3)  # 所有的name_id 如(('201901',), ('201902',), ('201903',), ('201904',))
        sql4 = "SELECT name_id FROM sign where date = " + "'" + str(date_to_find) + "'"  # 从sign表中找到所有当日的name_id

        cur.execute(sql4)
        u4 = cur.fetchall()
        print(u4)  # 已签到的name_id 如(('201901',),)
        sql5 = "SELECT name_id FROM business_trip where date = " + "'" + str(
            date_to_find) + "'" + "and result = 'agree'"

        cur.execute(sql5)
        u5 = cur.fetchall()
        print(u5)  # 未签到的name_id处于申请出差并同意的name_id，如(('201902',),)
        sql6 = "SELECT name_id FROM dayoff where date = " + "'" + str(date_to_find) + "'" + "and result = 'agree'"
        cur.execute(sql6)
        u6 = cur.fetchall()
        print(u6)  # 未签到且未同意出差的name_id但同意请假的name_id，如(('201904',),)

        find = []  # 存储每个name_id是否已签到的标记，已签到为1，未签到为0
        t1 = []
        for i in range(len(u3)):
            if len(u4) == 0:  # 若今日未有人签到，则u4为空，无法进入下面的循环，故需提前判断
                find.append(0)
            else:
                for j in range(len(u4)):
                    print(u3[i][0])
                    if u3[i][0] == u4[j][0]:
                        print(666)
                        # find[i] = 1
                        print(find)
                        find.append(1)  # 已签到
                        print(find)
                        break
                    if j == len(u4)-1:
                        find.append(0)  # 未签到
                    print(find)
            t1.append([u3[i][0], find[i]])
        print(t1)  # 找到每个name_id对应今日是否已签到的列表 如[['201901', 1], ['201902', 0], ['201903', 0], ['201904', 0]]
        t_all_name_id = []
        t_original_unsigned = []
        for i in range(len(t1)):
            t_all_name_id.append(t1[i][0])
            if t1[i][1] == 0:
                t_original_unsigned.append(t1[i][0])
        print(t_all_name_id)  # 所有员工的name_id存到列表中，如['201901', '201902', '201903', '201904']   *******************
        t_signed = list(set(t_all_name_id) - set(t_original_unsigned))  # 将已签到的name_id存到列表中
        print(t_original_unsigned)  # 将未签到的name_id存到列表中，如['201902', '201903', '201904']
        t_business = []
        for i in range(len(u5)):
            t_business.append(u5[i][0])
        print(t_business)  # 将未签到但出差且同意的name_id存到列表中，如['201902']       **********************
        t4 = list(set(t_original_unsigned) - set(t_business))
        print(t4)  # 将未签到且未同意出差的name_id存到列表中，如['201903', '201904']
        t_dayoff = []
        for i in range(len(u6)):
            t_dayoff.append(u6[i][0])
        print(t_dayoff)  # 将未签到且未同意出差但同意请假的name_id存到列表中，如['201904']  ************************
        t_unsigned = list(set(t4) - set(t_dayoff))
        print(t_unsigned)  # 将未签到且未同意出差或请假的name_id存到列表中，即未签到，如['201903']  ********************

        # 先判断签到后是否已签退，进而填写签退信息
        u_all = []
        now_time = datetime.datetime.now()
        datetime_nowtime = now_time.strftime("%Y-%m-%d")
        sql11 = "SELECT * FROM sign WHERE date = "+"'"+str(date_to_find)+"'"
        print(sql11)
        cur.execute(sql11)
        u11 = cur.fetchall()
        print(u11)

        if date_to_find==datetime_nowtime:
            for i in range(len(u11)):
                u_temp = ()
                # 计算签到后是否未签退
                now_time = datetime.datetime.now()
                off_set = u11[i][4]
                off_set_time = now_time + off_set
                off_set_time = time.mktime(off_set_time.timetuple())
                now_time = time.mktime(now_time.timetuple())
                second = off_set_time - now_time
                if second <= 0:   #规定未签退时时间为00:00:00
                    u1_var = list(u11[i])
                    u1_var[4] = "未签退"
                    u_temp += tuple(u1_var)
                else:
                    u_temp += u11[i]
                u_temp += u2[0]
                u_all += [u_temp, ]

        else:
            for i in range(len(u11)):
                u_temp = ()
                u_temp += u11[i]
                u_temp += u2[0]
                u_all += [u_temp, ]
        print(u_all)
        # 再在没有签到的name_id中进行判断
        for i in list(set(t_all_name_id) - set(t_signed)):
            print(i)
            sql0 = "SELECT name,name_id FROM information WHERE name_id =" + str(i)
            # print(sql0)
            cur.execute(sql0)
            # 如果出差并同意
            if (i in t_business):
                u_business = cur.fetchall()
                print(u_business)
                u_business1 = u_business[0] + (date_to_find, '出差', '', '', '')
                print(u_business1)
                u_all += [u_business1, ]
                print(u_all)
            # 如果请假并同意
            elif (i in t_dayoff):
                u_dayoff = cur.fetchall()
                print(u_dayoff)
                u_dayoff1 = u_dayoff[0] + (date_to_find, '请假', '', '', '')
                print(u_dayoff1)
                u_all += [u_dayoff1, ]
                print(u_all)
            # 未出差或请假  即未签到
            else:
                u_unsigned = cur.fetchall()
                print(u_unsigned)
                u_unsigned1 = u_unsigned[0] + (date_to_find, '未签到', '', '', '')
                print(u_unsigned1)
                u_all += [u_unsigned1, ]
                print(u_all)
        u_all.sort(key=lambda x: int(x[1]))
        print(u_all)
        conn.close()
        return render_template('check_signin.html', u=u_all)

    else:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()

        sql1 = "SELECT * FROM sign"
        cur.execute(sql1)
        u1 = cur.fetchall()
        sql2 = "SELECT sign_in_time,sign_out_time FROM setting"
        cur.execute(sql2)
        u2 = cur.fetchall()

        # 遍历当天所有name_id的签到信息，若未在sign表中找到该name_id，在查询business表和dayoff表，合并单元格为“未签到”/“出差”/“请假”
        sql3 = "SELECT name_id FROM information"  # 从information表中先找到所有的name_id
        cur.execute(sql3)
        u3 = cur.fetchall()
        print(u3)  # 所有的name_id 如(('201901',), ('201902',), ('201903',), ('201904',))
        now_time = datetime.datetime.now()
        datetime_nowtime = now_time.strftime("%Y-%m-%d")  # 当日的日期，str类型 (2019-7-16)
        sql4 = "SELECT name_id FROM sign where date = " + "'" + str(datetime_nowtime) + "'"  # 从sign表中找到所有当日的name_id
        print(sql4)
        cur.execute(sql4)
        u4 = cur.fetchall()
        print(u4)  # 已签到的name_id 如(('201901',),)
        sql5 = "SELECT name_id FROM business_trip where date = " + "'" + str(
            datetime_nowtime) + "'" + "and result = 'agree'"
        print(sql5)
        cur.execute(sql5)
        u5 = cur.fetchall()
        print(u5)  # 未签到的name_id处于申请出差并同意的name_id，如(('201902',),)
        sql6 = "SELECT name_id FROM dayoff where date = " + "'" + str(datetime_nowtime) + "'" + "and result = 'agree'"
        cur.execute(sql6)
        u6 = cur.fetchall()
        print(u6)  # 未签到且未同意出差的name_id但同意请假的name_id，如(('201904',),)

        find = []  # 存储每个name_id是否已签到的标记，已签到为1，未签到为0
        t1 = []
        for i in range(len(u3)):
            if len(u4)==0:          #若今日未有人签到，则u4为空，无法进入下面的循环，故需提前判断
                find.append(0)
            else:
                for j in range(len(u4)):
                    if u3[i][0] == u4[j][0]:
                        # find[i] = 1
                        find.append(1)  # 已签到
                        break
                    if j == len(u4)-1:
                        find.append(0)  #未签到
            t1.append([u3[i][0], find[i]])
        print(t1)  # 找到每个name_id对应今日是否已签到的列表 如[['201901', 1], ['201902', 0], ['201903', 0], ['201904', 0]]
        t_all_name_id = []
        t_original_unsigned = []
        for i in range(len(t1)):
            t_all_name_id.append(t1[i][0])
            if t1[i][1] == 0:
                t_original_unsigned.append(t1[i][0])
        print(t_all_name_id)  # 所有员工的name_id存到列表中，如['201901', '201902', '201903', '201904']   *******************
        t_signed = list(set(t_all_name_id) - set(t_original_unsigned))  # 将已签到的name_id存到列表中
        print(t_original_unsigned)  # 将未签到的name_id存到列表中，如['201902', '201903', '201904']
        t_business = []
        for i in range(len(u5)):
            t_business.append(u5[i][0])
        print(t_business)  # 将未签到但出差且同意的name_id存到列表中，如['201902']       **********************
        t4 = list(set(t_original_unsigned) - set(t_business))
        print(t4)  # 将未签到且未同意出差的name_id存到列表中，如['201903', '201904']
        t_dayoff = []
        for i in range(len(u6)):
            t_dayoff.append(u6[i][0])
        print(t_dayoff)  # 将未签到且未同意出差但同意请假的name_id存到列表中，如['201904']  ************************
        t_unsigned = list(set(t4) - set(t_dayoff))
        print(t_unsigned)  # 将未签到且未同意出差或请假的name_id存到列表中，即未签到，如['201903']  ********************

        # 先判断签到后是否已签退，进而填写签退信息
        u_all = []

        sql12 = "SELECT * FROM sign WHERE date = " + "'" + str(datetime_nowtime) + "'"
        print(sql12)
        cur.execute(sql12)
        u12 = cur.fetchall()
        print(u12)
        for i in range(len(u12)):
            u_temp = ()
            # 计算签到后是否未签退
            now_time = datetime.datetime.now()
            off_set = u12[i][4]
            off_set_time = now_time + off_set
            off_set_time = time.mktime(off_set_time.timetuple())
            now_time = time.mktime(now_time.timetuple())
            second = off_set_time - now_time
            if second < 0:
                u1_var = list(u12[i])
                u1_var[4] = "未签退"
                u_temp += tuple(u1_var)
            else:
                u_temp += u12[i]
            u_temp += u2[0]
            u_all += [u_temp, ]

        # 再在没有签到的name_id中进行判断
        for i in list(set(t_all_name_id) - set(t_signed)):
            print(i)
            sql0 = "SELECT name,name_id FROM information WHERE name_id =" + str(i)
            cur.execute(sql0)
            # 如果出差并同意
            if (i in t_business):
                u_business = cur.fetchall()
                print(u_business)
                u_business1 = u_business[0] + (datetime_nowtime, '出差', '', '', '')
                print(u_business1)
                u_all += [u_business1, ]
                print(u_all)
            # 如果请假并同意
            elif (i in t_dayoff):
                u_dayoff = cur.fetchall()
                print(u_dayoff)
                u_dayoff1 = u_dayoff[0] + (datetime_nowtime, '请假', '', '', '')
                print(u_dayoff1)
                u_all += [u_dayoff1, ]
                print(u_all)
            # 未出差或请假  即未签到
            else:
                u_unsigned = cur.fetchall()
                print(u_unsigned)
                u_unsigned1 = u_unsigned[0] + (datetime_nowtime, '未签到', '', '', '')
                print(u_unsigned1)
                u_all += [u_unsigned1, ]
                print(u_all)
        u_all.sort(key=lambda x: int(x[1]))

        conn.close()
        return render_template('check_signin.html', u=u_all)

#|------------------------------------userinfo------------------------------------|
@app.route('/admin/userinfo/delete/',methods=['POST'])
def userinfo_delete():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    cur = conn.cursor()
    del_id = request.form.get('del')
    alert = ""
    sql3 = "select name_id from information"
    cur.execute(sql3)
    u3 = cur.fetchall()

     # delete
    for i in range(len(u3)):
         if del_id == u3[i][0]:
            sql4 = "DELETE FROM information WHERE name_id =" + str(del_id)
            cur.execute(sql4)
            path1 = ".//static//pic//"+str(del_id)+'.png'
            os.remove(path1)
            alert = "alert('delete successfully')"
            sql1 = "SELECT name,name_id,gender,birth,address,position,password FROM information"
            cur.execute(sql1)
            u1 = cur.fetchall()
            u1 = list(u1)
            for i in range(len(u1)):
                path = "pic//" + str(u1[i][1]) + '.png'
                u1[i] += (path,)
            break
         else:
             sql1 = "SELECT name,name_id,gender,birth,address,position,password FROM information"
             cur.execute(sql1)
             u1 = cur.fetchall()
             u1 = list(u1)
             for i in range(len(u1)):
                 path = "pic//" + str(u1[i][1]) + '.png'
                 u1[i] += (path,)
             alert = "alert('failed')"
    conn.commit()
    conn.close()
    return render_template('user_info.html', u=u1, alert=alert)

@app.route('/admin/userinfo/save/',methods=['POST','GET'])
def userinfo_save():
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()
        sql3 = "SELECT name_id FROM information"
        cur.execute(sql3)
        name_id_all = cur.fetchall()
        for id in range(len(name_id_all)):
            print(name_id_all[id][0])
            name_id = request.form.get(str(name_id_all[id][0])+' ')
            if name_id:
                name_id = name_id.rstrip(' ')
                name_id_pre = name_id_all[id][0]
                break
        name = request.form.get('name')
        gender = request.form.get('gender')
        birth = request.form.get('birth')
        address = request.form.get('address')
        position = request.form.get('position')
        password = request.form.get('password')
        if password:
            password = password.rstrip(' ')
        f = request.files.get('pic1')
        path = ".//static//pic//"+str(name_id)+'.png'
        if f:
            f.save(path)
        if birth:
            sql2 = "update information set name='%s', name_id='%s', gender='%s', birth='%s', address='%s', position='%s', password='%s' WHERE name_id='%s'" % (name, name_id, gender, birth, address, position, password, name_id_pre)
        else:
            sql2 = "update information set name='%s', name_id='%s', gender='%s', address='%s', position='%s', password='%s'WHERE name_id='%s'" % (name, name_id, gender, address, position, password, name_id_pre)
        cur.execute(sql2)
        sql1 = "SELECT name,name_id,gender,birth,address,position,password FROM information"
        cur.execute(sql1)
        u1 = cur.fetchall()
        u1 = list(u1)
        for i in range(len(u1)):
            path = "pic//" + str(u1[i][1]) + '.png'
            u1[i] += (path,)
        conn.commit()
        conn.close()
        u1.sort(key=lambda x: int(x[1]))
        return render_template('user_info.html',u=u1,alert="")

@app.route('/admin/userinfo/',methods=['POST','GET'])
def userinfo_write():
    #write
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()
        name = request.form.get('name')
        name_id = request.form.get('num')
        gender = request.form.get('gender')
        birth = request.form.get('birth')
        address = request.form.get('home')
        job = request.form.get('job')
        password = request.form.get('pwd')
        photo = request.files.get('pic')
        path = ".//static//pic//" + str(name_id) + '.png'


        sql3 = "select name_id from information"
        cur.execute(sql3)
        u3 = cur.fetchall()
        alert = ""
        for i in range(len(u3)):
            if u3[i][0] == name_id:
                alert = "window.alert('该员工ID已存在，添加失败！')"
                break
        if alert == "":
            photo.save(path)
            cur = conn.cursor()
            sql2 = "INSERT INTO information VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (name, name_id, gender, birth, address, job, password)
            print(sql2)
            cur.execute(sql2)
        sql1 = "SELECT name,name_id,gender,birth,address,position,password FROM information"
        cur.execute(sql1)
        u1 = cur.fetchall()
        u1 = list(u1)
        for i in range(len(u1)):
            path = "pic//" + str(u1[i][1]) + '.png'
            u1[i] += (path,)
        u1.sort(key=lambda x:int(x[1]))

        conn.commit()
        conn.close()
        return render_template('user_info.html',u=u1, alert=alert)
    print(1)
    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
    # read
    cur = conn.cursor()
    sql1 = "SELECT name,name_id,gender,birth,address,position,password FROM information"
    cur.execute(sql1)
    u1 = cur.fetchall()
    u1 = list(u1)
    for i in range(len(u1)):
        path = "pic//" + str(u1[i][1]) + '.png'
        u1[i] += (path,)
    u1.sort(key=lambda x:int(x[1]))
    conn.close()
    return render_template('user_info.html', u=u1)
#|------------------------------------messagelist------------------------------------|
@app.route('/admin/messagelist',methods=['GET'])
def user_info():
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        # read
        cur = conn.cursor()
        sql1 = "SELECT * FROM business_trip"
        sql2 = "SELECT * FROM retroactive"
        sql3 = "SELECT * FROM dayoff"
        cur.execute(sql1)
        u1 = cur.fetchall()
        cur.execute(sql2)
        u2 = cur.fetchall()
        cur.execute(sql3)
        u3 = cur.fetchall()
        u1 = list(u1)
        u2 = list(u2)
        u3 = list(u3)
        u1.sort(key=lambda x:x[0])
        u1.reverse()
        u2.sort(key=lambda x: x[0])
        u2.reverse()
        u3.sort(key=lambda x: x[0])
        u3.reverse()
        conn.commit()
        conn.close()
        return render_template('message_list.html', u1=u1,u2=u2,u3=u3)

@app.route('/admin/messagelist/business', methods=['GET', 'POST'])
def user_info_bussiness():
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()
        sql4 = "SELECT id FROM business_trip"
        cur.execute(sql4)
        u3 = cur.fetchall()
        for each in range(len(u3)):
            if request.form.get(str(u3[each][0])) == 'agree':
                name = u3[each][0]
                result = 'agree'
                break
            elif request.form.get(str(u3[each][0])) == 'refuse':
                name = u3[each][0]
                result = 'refuse'
                break
        sql2 = "UPDATE business_trip SET result = '" + str(result) + "' WHERE  id = '" + str(name) + "'"
        cur.execute(sql2)
        sql1 = "SELECT * FROM business_trip"
        sql2 = "SELECT * FROM retroactive"
        sql3 = "SELECT * FROM dayoff"
        cur.execute(sql1)
        u1 = cur.fetchall()
        cur.execute(sql2)
        u2 = cur.fetchall()
        cur.execute(sql3)
        u3 = cur.fetchall()
        u1 = list(u1)
        u2 = list(u2)
        u3 = list(u3)
        u1.sort(key=lambda x: int(x[0]))
        u1.reverse()
        u2.sort(key=lambda x: int(x[0]))
        u2.reverse()
        u3.sort(key=lambda x: int(x[0]))
        u3.reverse()
        conn.commit()
        conn.close()
        return render_template('message_list.html', u1=u1, u2=u2, u3=u3)

@app.route('/admin/messagelist/retroactive', methods=['GET', 'POST'])
def user_info_retroactive():
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()
        sql4 = "SELECT id FROM retroactive"
        cur.execute(sql4)
        u3 = cur.fetchall()
        for each in range(len(u3)):
            if request.form.get(str(u3[each][0])) == 'agree':
                name = u3[each][0]
                result = 'agree'
                break
            elif request.form.get(str(u3[each][0])) == 'refuse':
                name = u3[each][0]
                result = 'refuse'
                break
        sql2 = "UPDATE retroactive SET result = '" + str(result) + "' WHERE  id = '" + str(name) + "'"
        cur.execute(sql2)
        sql1 = "SELECT * FROM business_trip"
        sql2 = "SELECT * FROM retroactive"
        sql3 = "SELECT * FROM dayoff"
        cur.execute(sql1)
        u1 = cur.fetchall()
        cur.execute(sql2)
        u2 = cur.fetchall()
        cur.execute(sql3)
        u3 = cur.fetchall()
        u1 = list(u1)
        u2 = list(u2)
        u3 = list(u3)
        u1.sort(key=lambda x: x[0])
        u1.reverse()
        u2.sort(key=lambda x: x[0])
        u2.reverse()
        u3.sort(key=lambda x: x[0])
        u3.reverse()
        conn.commit()
        conn.close()
        return render_template('message_list.html', u1=u1, u2=u2, u3=u3)

@app.route('/admin/messagelist/dayoff', methods=['GET', 'POST'])
def user_info_dayoff():
    if request.method == 'POST':
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='ci', charset='utf8')
        cur = conn.cursor()
        sql4 = "SELECT id FROM dayoff"
        cur.execute(sql4)
        u3 = cur.fetchall()
        for each in range(len(u3)):
            if request.form.get(str(u3[each][0])) == 'agree':
                name = u3[each][0]
                result = 'agree'
                break
            elif request.form.get(str(u3[each][0])) == 'refuse':
                name = u3[each][0]
                result = 'refuse'
                break
        sql2 = "UPDATE dayoff SET result = '" + str(result) + "' WHERE  id = '" + str(name) + "'"
        cur.execute(sql2)
        sql1 = "SELECT * FROM business_trip"
        sql2 = "SELECT * FROM retroactive"
        sql3 = "SELECT * FROM dayoff"
        cur.execute(sql1)
        u1 = cur.fetchall()
        cur.execute(sql2)
        u2 = cur.fetchall()
        cur.execute(sql3)
        u3 = cur.fetchall()
        u1 = list(u1)
        u2 = list(u2)
        u3 = list(u3)
        u1.sort(key=lambda x: int(x[0]))
        u1.reverse()
        u2.sort(key=lambda x: int(x[0]))
        u2.reverse()
        u3.sort(key=lambda x: int(x[0]))
        u3.reverse()
        conn.commit()
        conn.close()
        return render_template('message_list.html', u1=u1, u2=u2, u3=u3)



if __name__ == '__main__':
    app.run()
