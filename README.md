## 考勤系统
这里使用html,css,js写前端。python语言使用flask框架写后端。
# 文件说明：
static文件夹：放置各种js,css,images等各种资源
templates文件夹：放置各种静态页面
faceface_identify.py:人脸识别代码
PunchVerification.py：地理位置查询
login.py:主函数
# 使用方法：
使用pycharm运行login.py。

# 注意：
1.需要自行设置数据库，后续将数据库模板上传上来。
2.不设置数据库只能看到登陆界面，要想进入主题界面，可将def login():
    return render_template('login.html')
    改为：
    def login():
    return render_template('index.html')
3.直接打开html是看不到特效的，因为flask的限制，html中引入外部图片等操作是和原来不一样的，所以要运行login.py。
