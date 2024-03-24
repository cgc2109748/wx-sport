from flask import jsonify, request
from app.models.user import User
from app import app 
from datetime import datetime
import base64
import json
from Cryptodome.Cipher import AES

# 用户注册
@app.route('/user/save', methods=['POST'])
def set_data():
    print('正在保存用户数据::::::', request.json)
    try:
       
        data = request.json  # 获取传入的 JSON 数据
        openid = data.get('openid')

        if openid is None:
            return jsonify({'error': '缺少 openid'}), 400

        user = User.objects(openid=openid).first()
        if user:
            # 更新用户信息
            user.update(**data)
            return jsonify({'message': '用户信息更新成功'}), 200
        else:
            # 新增用户
            new_user = User(**data)
            new_user.save()
            return jsonify({'message': '新用户添加成功'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# 用户签到
@app.route('/user/signIn', methods=['POST'])
def sign_in():
    try:
        # 假设从请求中获取用户的 openid
        openid = request.json.get('openid')
        user = User.objects(openid=openid).first()

        if user is None:
            return jsonify({'error': '用户不存在'}), 500

        # 检查今天是否已经签到
        today = datetime.now().strftime('%Y-%m-%d')
        if today in user.signInRecords:
            return jsonify({'error': '今日已签到！'}), 500

        # 添加签到记录
        user.signInRecords.append(today)
        user.integral += 1  # 假设每次签到增加 1 积分
        user.save()

        return jsonify({'message': '签到成功！', 'integral': user.integral}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 用户查询
@app.route('/user/get', methods=['GET'])
def get_user_info():
    try:
        openid = request.args.get('openid')
        if not openid:
            return jsonify({'error': 'Missing openid'}), 500

        user = User.objects(openid=openid).first()
        if not user:
            return jsonify({'error': 'User not found'}), 500

        data = {
            'openid': user.openid,
            'nickName': user.nickName,
            'avatarUrl': user.avatarUrl,
            'city': user.city,
            'country': user.country,
            'gender': user.gender,
            'language': user.language,
            'province': user.province,
            'integral': user.integral,
            'signInRecords': user.signInRecords
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 解密用户的运动数据
def decrypt(encryptedData, sessionKey, iv):
    # base64 decode
    sessionKey = base64.b64decode(sessionKey)
    encryptedData = base64.b64decode(encryptedData)
    iv = base64.b64decode(iv)

    cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
    decryptedData = cipher.decrypt(encryptedData)
    decryptedData = unpad(decryptedData)

    return decryptedData

def unpad(s):
    return s[:-ord(s[len(s)-1:])]

    # padding = s[-1]
    # return s[:-padding]

@app.route('/user/decryptRunData', methods=['POST'])
def decryptRunData():
    try:
        # 从请求中获取 encryptedData 和 sessionKey
        appId = 'wx0e882c95b6e81b99'
        encryptedData = request.json.get('encryptedData')
        sessionKey = request.json.get('sessionKey')
        iv = request.json.get('iv')
        # print('encryptedData: ', encryptedData)
        # print('sessionKey: ', sessionKey)
        # print('iv: ', iv)

        decryptedData = decrypt(encryptedData, sessionKey, iv)
        print('decryptedData1111: ', decryptedData)
        # print('decryptedData2222: ', decryptedData.decode('utf-8'))
        # if decryptedData['watermark']['appid'] != appId:
        #     raise Exception('Invalid Buffer')

        # 返回解密运动数据
        return decryptedData
    except Exception as e:
        return jsonify({'error': str(e)}), 500