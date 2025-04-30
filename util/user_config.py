import os
import configparser


class UserConfig:
    """
    用于读取和管理 user.ini 文件中的用户信息
    """
    def __init__(self, filepath="user.ini"):
        """
        初始化 UserConfig 类
        :param filepath: user.ini 文件的路径
        """
        self.filepath = filepath
        self.parser = configparser.ConfigParser()
        if os.path.exists(self.filepath):
            self.parser.read(self.filepath, encoding="utf-8")
        else:
            raise FileNotFoundError(f"配置文件 {self.filepath} 不存在！")

    def get_user_info(self, section="user1"):
        """
        获取指定节的用户信息
        :param section: user.ini 中的节名，例如 "user1"
        :return: 包含 username, uid, sid 的字典
        """
        if section not in self.parser.sections():
            raise ValueError(f"节 [{section}] 不存在于 {self.filepath} 中！")
        return {
            "username": self.parser[section].get("username", ""),
            "uid": self.parser[section].get("uid", ""),
            "sid": self.parser[section].get("sid", ""),
        }

    def add_user_info(self, section, username, uid, sid):
        """
        添加新的用户信息到 user.ini 文件
        :param section: 新用户的节名，例如 "user2"
        :param username: 用户名
        :param uid: 用户的 UID
        :param sid: 用户的 SID
        """
        if section in self.parser.sections():
            raise ValueError(f"节 [{section}] 已存在于 {self.filepath} 中！")
        self.parser.add_section(section)
        self.parser.set(section, "username", username)
        self.parser.set(section, "uid", str(uid))
        self.parser.set(section, "sid", sid)
        self.save()

    def update_user_info(self, section, username=None, uid=None, sid=None):
        """
        更新已有用户的信息
        :param section: 要更新的节名
        :param username: 新的用户名（可选）
        :param uid: 新的 UID（可选）
        :param sid: 新的 SID（可选）
        """
        if section not in self.parser.sections():
            raise ValueError(f"节 [{section}] 不存在于 {self.filepath} 中！")
        if username:
            self.parser.set(section, "username", username)
        if uid:
            self.parser.set(section, "uid", str(uid))
        if sid:
            self.parser.set(section, "sid", sid)
        self.save()

    def save(self):
        """
        将更改保存到 user.ini 文件
        """
        with open(self.filepath, "w", encoding="utf-8") as configfile:
            self.parser.write(configfile)