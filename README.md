# 兰大悦跑圈模拟脚本

> 支持账号密码和手机号验证码登录
> 5秒钟上传完跑步记录  
> 本项目由 [github 上的 TarikVon/LZURunningHelper](https://github.com/TarikVon/LZURunningHelper) 改造而来。  

## 配置文件说明

- **config.ini**  
  - [Joyrun]  
    - record_type：可设置为以下值  
      - dongcao：东操  
      - xicao：西操  
      - random (默认)：随机  

- **user.ini**  
  - 存储 sid 和 uid 信息  
  - username：用于区分多用户  

## 环境要求

- 需要 Python ≥ 3.6（示例中使用 3.8 测试较多，3.12 理论可行，但未测试）  
- 需要在项目根目录终端执行：  
  ```bash
  pip3 install -r requirements.txt
  ```  
- 需要新建 cache 文件夹（用于存储文件缓存）。该文件夹可为空。  

## 使用说明

1. 每次切换账号后记得保存 config.ini，否则会仍然使用原账号。  
2. 如果运行时没有使用 “-B”，需要手动删除根目录及部分子目录中的 __pycache__ 文件夹。  
3. 首次跑步时无时间限制，但如果第二次跑步用时 10 分钟，需要间隔 10 分钟以上后再次执行脚本，否则会被判定异常，不计入成绩。  
4. 如果登录手机端后 sid 会立刻失效，需要重新通过验证码获取新的 sid 值。

### 交互脚本运行

- 在项目根目录，执行：  
  ```bash
  python -B main.py
  ```  
- 将根据提示选择：  
  输入1: 从 config.ini 获取账号密码登录  
  输入2: 从 user.ini 获取 uid、sid 登录  

### 通过验证码获取 uid、sid

1. 打开 login.py，在代码中填入手机号和验证码；确保手机上未登录悦跑圈，否则 sid 会失效。  
2. 成功后，login.py 的输出中会打印当前的 sid、uid。  
3. 将获得的 sid、uid 填写到 user.ini 相应的 [userX] 节点下，并记住该 username。  
4. 再次执行：  
   ```bash
   python -B main.py
   ```
   选择 2，输入上面的 username，即可使用 sid、uid 登录。

---

## 日志示例

### 1. 使用 user.ini 内的 uid、sid 成功上传记录

以下是查看日志后输出的关键片段 (部分字段已脱敏)：

```plaintext
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
    "weixinurl": ...,
    "fraudSubStatus": 0,
    "multipleUpload": false
}
```

### 2. sid 过期触发重试

```plaintext
请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): 2
使用 user.ini 内的登录信息...
请输入要登录的用户名(例如 'zhs'): zzh
已匹配到节 [user2] -> uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[INFO] main, 2025-04-30 09:44:10, Running Joyrun Client [2018.10.01] with user.ini
[DEBUG] joyrun, 2025-04-30 09:44:10, Using existing uid/sid from user.ini
[DEBUG] joyrun, 2025-04-30 09:44:10, Using override uid/sid from main.py, uid=xxxxxxxxx, sid=xxxxxxxxxxxxxxxxxxx
[DEBUG] joyrun, 2025-04-30 09:44:13, sid invalid, retry 1
Traceback (most recent call last):
  File "C:\Users\zzh\Downloads\LZURunningHelper-main\Joyrun\client.py", ...
    ...
Joyrun.error.JoyrunSidInvalidError: sid invalid
```

该错误表示 sid 已失效，需要重新获取。

### 3. 使用 config.ini 内的 username/password 成功登录并上传

```plaintext
请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): 1
使用 config.ini 内的登录信息 (跳过 uid/sid) ...
[INFO] main, 2025-04-30 09:45:57, Running Joyrun Client [2018.10.01] with config.ini
[DEBUG] joyrun, 2025-04-30 09:45:57, Using StudentID=xxxxxxxxxxxx@lzu.edu.cn, Password=123456 from config.ini
[DEBUG] joyrun, 2025-04-30 09:45:57, Using StudentID/Password login
[DEBUG] joyrun, 2025-04-30 09:45:59, request.url = ...
[DEBUG] joyrun, 2025-04-30 09:45:59, response.json = {
    "ret": "0",
    "msg": "成功",
    "data": {
        "sid": "不告诉你嘻嘻",
        "user": {
            "uid": "这个也不告诉你喵",
            ...
        }
    }
}
[DEBUG] joyrun, 2025-04-30 09:46:00, request.url = https://api.thejoyrun.com/po.aspx
[DEBUG] joyrun, 2025-04-30 09:46:00, response.json = {
    "fid": 1087997015,
    "postRunId": 990556795,
    "ret": "0",
    "msg": "发布成功",
    "sid": "...",
    "fraud": "0",
    ...
}
```

---
