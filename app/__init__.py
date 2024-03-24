from flask import Flask, send_from_directory
from flask_cors import CORS
from mongoengine import connect
import os

app = Flask(__name__)

# 配置和初始化...
CORS(app, resources=r'/*',)
connect(db='wx-sport-server', host='localhost', port=27017)

# 导入控制器模块以注册路由和视图函数
from app.controllers import user_controller, sport_controller

#静态文件服务
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('filename:', filename)
    file_path = os.path.join('uploads', filename)
    print('file_path:', file_path)
    print('App root path:', app.root_path)
    if os.path.exists(file_path):
        print('File exists')
    else:
        print('File does not exist')
    return send_from_directory('../uploads', filename)
