#### python
# filepath: c:\Users\zzh\Downloads\LZURunningHelper-main\login.py
import time
import requests
from hashlib import md5

def get_md5_data(data):
    return md5(str(data).encode("utf-8")).hexdigest().upper()

class JoyrunAuth:
    def __init__(self, uid=0, sid=""):
        self.params = {}
        self.uid = uid
        self.sid = sid

    def reload(self, params={}, uid=0, sid=""):
        self.params = params
        if uid and sid:
            self.uid = uid
            self.sid = sid
        return self

    @classmethod
    def __get_signature(cls, params, uid, sid, salt):
        if not uid:
            uid = sid = ""
        pre_string = "{params_string}{salt}{uid}{sid}".format(
            params_string="".join(
                "".join((k, str(v))) for k, v in sorted(params.items())
            ),
            salt=salt,
            uid=str(uid),
            sid=str(sid),
        )
        return get_md5_data(pre_string)

    @classmethod
    def get_signature_v1(cls, params, uid=0, sid=""):
        return cls.__get_signature(params, uid, sid, "1fd6e28fd158406995f77727b35bf20a")

    @classmethod
    def get_signature_v2(cls, params, uid=0, sid=""):
        return cls.__get_signature(params, uid, sid, "0C077B1E70F5FDDE6F497C1315687F9C")

    def __call__(self, r):
        params = self.params.copy()
        params["timestamp"] = int(time.time())

        signV1 = self.get_signature_v1(params, self.uid, self.sid)
        signV2 = self.get_signature_v2(params, self.uid, self.sid)

        r.headers["_sign"] = signV2

        if r.method == "GET":
            r.prepare_url(
                r.url, params={"signature": signV1, "timestamp": params["timestamp"]}
            )
        elif r.method == "POST":
            params["signature"] = signV1
            r.prepare_body(data=params, files=None)
        return r

class Joyrun:
    base_url = "https://api.thejoyrun.com"

    def __init__(self, user_name="", identifying_code="", uid=0, sid=""):
        self.user_name = user_name
        self.identifying_code = identifying_code
        self.uid = uid
        self.sid = sid

        self.session = requests.Session()
        self.session.headers.update(self.base_headers)
        self.session.headers.update(self.device_info_headers)

        self.auth = JoyrunAuth(self.uid, self.sid)
        if self.uid and self.sid:
            self.__update_loginInfo()

    @property
    def base_headers(self):
        return {
            "Accept-Language": "en_US",
            "User-Agent": "okhttp/3.10.0",
            "Host": "api.thejoyrun.com",
            "Connection": "Keep-Alive",
        }

    @property
    def device_info_headers(self):
        # 与原项目保持一致，以避免版本过旧的问题
        return {
            "MODELTYPE": "Xiaomi MI 5",
            "SYSVERSION": "8.0.0",
            "APPVERSION": "4.2.0",
        }

    def __update_loginInfo(self):
        self.auth.reload(uid=self.uid, sid=self.sid)
        # 这里可以根据需要更新 Cookie 或其他信息

    def login_by_phone(self):
        params = {
            "phoneNumber": self.user_name,
            "identifyingCode": self.identifying_code,
        }
        r = self.session.get(
            f"{self.base_url}//user/login/phonecode",
            params=params,
            auth=self.auth.reload(params),
        )
        login_data = r.json()
        if login_data["ret"] != "0":
            raise Exception(f'{login_data["ret"]}: {login_data["msg"]}')
        self.sid = login_data["data"]["sid"]
        self.uid = login_data["data"]["user"]["uid"]
        print(f"your uid: {self.uid}, your sid: {self.sid}")
        self.__update_loginInfo()


if __name__ == "__main__":
    # 示例：固定手机号与验证码
    phone = "输入你的手机号"
    code = "输入你获得的验证码"
    j = Joyrun(user_name=phone, identifying_code=code)
    j.login_by_phone()