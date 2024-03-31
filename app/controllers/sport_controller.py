from flask import jsonify, request
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from datetime import datetime
from app.models.sport import Sport
from app import app 

load_dotenv()

# 设置图片保存的路径
UPLOAD_FOLDER = 'uploads'
BASE_URL = os.getenv('BASE_URL')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 新增运动项目
@app.route('/sport/add', methods=['POST'])
def add_sport():
    try:
        data = request.form.to_dict()
        image = request.files.get('image')
        if image:
            filename = secure_filename(image.filename)
            save_path = os.path.join('uploads', filename)
            image.save(save_path)  # 保存图片到服务器
            path = BASE_URL + '/' + save_path
            print('path:', path)
            data['image'] = path  # 将图片路径存储在数据中

        data['createdAt'] = datetime.now().strftime('%Y-%m-%d')
        new_sport = Sport(**data)
        new_sport.save()
        return jsonify({'message': '新增运动项目成功'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 分页查询运动项目
@app.route('/sport/list', methods=['GET'])
def list_sports():
    try:
        page = request.args.get('page', 1, type=int)
        pageSize = request.args.get('pageSize', 10, type=int)
        offset = (page - 1) * pageSize

        sports = Sport.objects.skip(offset).limit(pageSize)
        total = Sport.objects.count()

        sports_data = [{
            'id': str(sport.id),
            'title': sport.title,
            'organizer': sport.organizer,
            'tags': sport.tags,
            'startDate': sport.startDate,
            'startTime': sport.startTime,
            'endDate': sport.endDate,
            'endTime': sport.endTime,
            'content': sport.content,
            'image': sport.image,
            'status': sport.status
        } for sport in sports]

        return jsonify({
            'results': sports_data,
            'total': total,
            'page': page,
            'pageSize': pageSize
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# 根据 id 查询运动项目
@app.route('/sport', methods=['GET'])
def get_sport():
    try:
        sportId = request.args.get('sportId')
        sport = Sport.objects.get(id=sportId)
        if sport:
            sport_data = {
                'id': str(sport.id),
                'title': sport.title,
                'organizer': sport.organizer,
                'tags': sport.tags,
                'startDate': sport.startDate,
                'startTime': sport.startTime,
                'endDate': sport.endDate,
                'endTime': sport.endTime,
                'content': sport.content,
                'image': sport.image,
                'status': sport.status
            }
            return jsonify(sport_data), 200
        else:
            return jsonify({'message': '运动项目不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 更新运动项目的审批状态
@app.route('/sport/approve', methods=['POST'])
def approve_sport():
    try:
        data = request.get_json()
        sport_id = data.get('sportId')
        new_status = data.get('status')

        sport = Sport.objects.get(id=sport_id)
        if sport:
            sport.status = new_status
            sport.save()
            return jsonify({'message': '运动项目审批状态更新成功'}), 200
        else:
            return jsonify({'message': '运动项目不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 删除运动项目
@app.route('/sport/delete/<sport_id>', methods=['DELETE'])
def delete_sport(sport_id):
    try:
        sport = Sport.objects.get(id=sport_id)  # 根据 ID 获取要删除的运动项目
        if not sport:
            return jsonify({'error': '运动项目不存在'}), 404

        sport.delete()  # 删除运动项目
        return jsonify({'message': '运动项目删除成功'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500