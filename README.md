本项目由github上的项目兰大悦跑大改而成(https://github.com/TarikVon/LZURunningHelper)
config.ini 文件内 record_type: 配置为使用的地图路径，可以设置以下的值：

record_type:
- dongcao: 东操
- xicao: 西操
- random (默认): 随机
需要python3.8的环境, 或者3.6可能也行, 3.12好像也可以, 未测试
需要手动在文件夹内的终端输入pip3 install -r requirements.txt
需要有cache文件夹,里面不需要有文件(使用手机号密码登陆需要有这个文件夹, 不需要有文件)
每次在终端运行python -B main.py
每次运行完之后想要切换账号保存config.ini, 否则还是原账号
如果上一次运行没有使用-B命令, 需要手动删除其中两个文件夹中的__pychche__文件夹
第一次刷没有限制, 但是如果第二次跑步用时10分钟, 必须要间隔10分钟以上, 不能说跑完了一次之后, 隔了十分钟就跑了二十分钟的跑步这样的
通过验证码可以获得账号的uid和sid, uid是固定不变的, sid获取后如果在手机上登陆就会立即改变, 需要重新通过验证码获取新值

使用方法: 
1,进入login.py , 将手机号和验证码输入代码中, 验证码使用手机号验证码登陆, 但是不要将验证码输入手机登陆, 手机先保持未登录的状态, 运行login.py , 如果手机号和验证码有效, login的输出会给出sid和uid
2, user.ini存储了sid和uid信息, username用于区分多用户, 将sid和uid黏贴到一个用户上, 记住你自定义的用户名
3, 运行python -B main.py (核心)
4, 如果选择1, 则使用config.ini的账号密码以登陆, 忽略user.ini, 适合没有绑定手机号的账号. 如果选择2, 使用user.ini的uid和sid登陆, 这样你输入刚刚记住的username, 如果用户名输入错误会提示用户不存在, 查找到就会开始上传记录, 适合手贱绑定了手机号的用户



以下是使用uid和sid上传记录成功的输出
以下所有的个人信息uid和sid已经被我删除
(c:\Users\zzh\Downloads\LZURunningHelper-main\.conda) C:\Users\zzh\Downloads\LZURunningHelper-main>python -B main.py
请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): 2
使用 user.ini 内的登录信息...
请输入要登录的用户名(例如 'zhs'): zzh
已匹配到节 [user2] -> uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[INFO] main, 2025-04-30 09:29:38, Running Joyrun Client [2018.10.01] with user.ini
[DEBUG] joyrun, 2025-04-30 09:29:38, Using existing uid/sid from user.ini
[DEBUG] joyrun, 2025-04-30 09:29:38, Using override uid/sid from main.py, uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[DEBUG] joyrun, 2025-04-30 09:29:39, request.url = https://api.thejoyrun.com/po.aspx
[DEBUG] joyrun, 2025-04-30 09:29:39, response.json = {
    "fid": 1087993022,
    "postRunId": 990553139,
    "ret": "0",
    "msg": "发布成功",
    "sid": "xxxxxxxxxxxxxxxxxxx",
    "fraud": "0",
    "lasttime": 1745976581,
    "weixinurl": "https://wap.thejoyrun.com/po_detail_v1_xxxxxxxxx_990553139_a0513c3556002c093dd77764504034ed013f01b1d1bed5dc08d2f39045881795a47a5b787251f94927c1ba82c0adb04bdaed5902.html",
    "fraudSubStatus": 0,
    "multipleUpload": false
}



以下是sid过期的输出示例
(c:\Users\zzh\Downloads\LZURunningHelper-main\.conda) C:\Users\zzh\Downloads\LZURunningHelper-main>python -B main.py
请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): 2
使用 user.ini 内的登录信息...
请输入要登录的用户名(例如 'zhs'): zzh
已匹配到节 [user2] -> uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[INFO] main, 2025-04-30 09:44:10, Running Joyrun Client [2018.10.01] with user.ini
[DEBUG] joyrun, 2025-04-30 09:44:10, Using existing uid/sid from user.ini
[DEBUG] joyrun, 2025-04-30 09:44:10, Using override uid/sid from main.py, uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[DEBUG] joyrun, 2025-04-30 09:44:13, sid invalid, retry 1
Traceback (most recent call last):
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 78, in return_wrapper
    return func(self, *args, **kwargs)
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 394, in upload_record
    respJson = self.post("/po.aspx", payload, auth=self.auth.reload(payload))
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 230, in post
    return self.__reqeust('POST', url, data=data, **kwargs)
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 216, in __reqeust
    raise JoyrunSidInvalidError("sid invalid")
Joyrun.error.JoyrunSidInvalidError: sid invalid

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "main.py", line 81, in <module>
    client.run()
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 422, in run
    self.upload_record(_record)
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 85, in return_wrapper
    self.login()
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", line 273, in login
    "username": self.userName,
AttributeError: 'JoyrunClient' object has no attribute 'userName'



以下是通过用户名和密码成功登陆的输出
个人的学号被我抹除
(c:\Users\zzh\Downloads\LZURunningHelper-main\.conda) C:\Users\zzh\Downloads\LZURunningHelper-main>python -B main.py
请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): 1
使用 config.ini 内的登录信息 (跳过 uid/sid) ...
[INFO] main, 2025-04-30 09:45:57, Running Joyrun Client [2018.10.01] with config.ini
[DEBUG] joyrun, 2025-04-30 09:45:57, Using StudentID=xxxxxxxxxxxx@lzu.edu.cn, Password=123456 from config.ini     
[DEBUG] joyrun, 2025-04-30 09:45:57, Using StudentID/Password login
[DEBUG] joyrun, 2025-04-30 09:45:59, request.url = https://api.thejoyrun.com//user/login/normal?username=xxxxxxxxxxxx%40lzu.edu.cn&pwd=E10ADC3949BA59ABBE56E057F20F883E&signature=FE4E8CC6785EBB4EA63FBD81A339B044&timestamp=1745977557
[DEBUG] joyrun, 2025-04-30 09:45:59, response.json = {
    "ret": "0",
    "msg": "成功",
    "data": {
        "sid": "不告诉你嘻嘻",
        "mailinfo": {
            "mail": "xxxxxxxxxxxx@lzu.edu.cn"
        },
        "user": {
            "uid": "这个也不告诉你喵",
            "verContent": null,
            "birthday": "19800101",
            "allsecond": "44679",
            "logtime": "1745919091",
            "weight": "60",
            "type": "1",
            "userrunlevel": "M1",
            "vipMemberState": 0,
            "lastRunTime": "1745916107000",
            "city": "广州",
            "allcalorie": "7861648",
            "height": "170",
            "allmeter": "126475",
            "province": "广东",
            "gender": "1",
            "friendcount": "2",
            "runnerlevel": "10",
            "mail": "xxxxxxxxxxxx@lzu.edu.cn",
            "headerurl": "",
            "allpo": "79",
            "regtime": "1728870792",
            "nick": "韦一敏",
            "userrunlevelachievedtime": "1741089771",
            "allzpo": "7",
            "faceurl": "",
            "introduction": "",
            "verType": 0
        }
    }
}
[DEBUG] joyrun, 2025-04-30 09:46:00, request.url = https://api.thejoyrun.com/po.aspx
[DEBUG] joyrun, 2025-04-30 09:46:00, response.json = {
    "fid": 1087997015,
    "postRunId": 990556795,
    "ret": "0",
    "msg": "发布成功",
    "sid": "58cd5e499783e1009847efa5d8f9543e",
    "fraud": "0",
    "lasttime": 1745977561,
    "weixinurl": "https://wap.thejoyrun.com/po_detail_v1_191028862_990556795_a23f4e7f791d6c53085aa6c30555ad72fc17238fe5c33526acf5414bea25def25d9f15ca5bc20a5810ffcc5b8cc3dd40a52d1b83.html",
    "fraudSubStatus": 0,
    "multipleUpload": false
}
