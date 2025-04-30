#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: main.py
#
# 项目运行主程序
#
import sys
import configparser
from optparse import OptionParser
from util import (
    Config, Logger,
    pretty_json,
    json,
    APPTypeError,
)

config = Config()
logger = Logger("main")

app = config.get('Base', 'APP')

if app == "Joyrun":
    from Joyrun import JoyrunClient as Client, __date__
else:
    raise APPTypeError("unsupported running APP -- %s !" % app)

parser = OptionParser(description="PKU running helper! Enjoy yourself!")
# 仅保留 -s 选项
parser.add_option("-s", "--start", help="start uploading job with %s Client" % app, action="store_false")

options, args = parser.parse_args()

# # 如果传入 -s 或未传入任何其它选项，则进入上传流程
# if options.start is not None:
#     try:
#         logger.info("Running %s Client [%s]" % (app, __date__))
#         client = Client()
#     except Exception as err:
#         logger.error("upload record failed !")
#         raise err
#     else:
#         logger.info("upload record success !")

# 交互式选择 —— config.ini 或 user.ini
choice = input("请选择登录方式 (1=从 config.ini 读取, 2=从 user.ini 读取): ").strip()

if choice == "1":
    print("使用 config.ini 内的登录信息 (跳过 uid/sid) ...")
    from Joyrun import JoyrunClient as Client, __date__
    logger.info("Running Joyrun Client [%s] with config.ini" % __date__)
    # 关键：在这里传 use_config=True
    client = Client(use_config=True)
    client.run()
elif choice == "2":
    print("使用 user.ini 内的登录信息...")
    user_name = input("请输入要登录的用户名(例如 'zhs'): ").strip()

    cfg = configparser.ConfigParser()
    cfg_path = "user.ini"
    cfg.read(cfg_path, encoding="utf-8")

    matched_section = None
    for section in cfg.sections():
        if cfg.has_option(section, "username") and cfg[section].get("username") == user_name:
            matched_section = section
            break

    if not matched_section:
        print(f"在 {cfg_path} 中找不到 username = {user_name} 的配置，请检查 user.ini。")
        sys.exit(1)

    user_uid = cfg[matched_section].get("uid")
    user_sid = cfg[matched_section].get("sid")
    print(f"已匹配到节 [{matched_section}] -> uid={user_uid}, sid={user_sid}")

    from Joyrun import JoyrunClient as Client, __date__
    logger.info("Running Joyrun Client [%s] with user.ini" % __date__)

    # 这里直接覆盖原先的配置，不再写回 user.ini
    client = Client(override_uid=user_uid, override_sid=user_sid)
    client.run()
else:
    print("无效选择，退出。")
    sys.exit(0)
