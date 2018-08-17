from flask import Flask, jsonify, abort, make_response, request, url_for,render_template,send_file,session
from flask import redirect
from flask_httpauth import HTTPBasicAuth
from Parameter import http_state,img_file_path
from Resnet_50.train import AiResNet50
from Resnet_50.test import AiResNet50Predict
from Parameter import httpResultWhiteMsg
from Parameter import Parameters
from datetime import timedelta
import io
import uuid
import os
import cv2

pass_urls=["static","login","logout"]
app = Flask(__name__)
# 图片最大为512M
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。
auth = HTTPBasicAuth()

#设置post请求中获取的图片保存的路径
UPLOAD_FOLDER = 'pic_tmp/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
else:
    pass
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html",tensorBoard_url="http://"+Parameters.host+":"+Parameters.TensorBoard_port+"/#scalars")

@app.route('/index')
def index_2():
    return index()

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session["user"]=="";
    return render_template("login.html")


@app.route('/login/user', methods=['POST'])
def login_user():
    user_name = request.form["user_name"]
    pass_word = request.form["pass_word"]
    print("login user:%s pass:%s"%(user_name,pass_word))
    if(user_name==Parameters.user  and pass_word==Parameters.pwd):
        session["user"]=user_name;
        print("login user:%s pass:%s is pass"%(user_name,pass_word))
        return redirect(url_for("index"))
    else:
        return httpResultWhiteMsg.send("用户名密码错误")


#返回目前平台能识别的所有类别
@app.route('/ai/class/getall', methods=['GET'])
def class_getall():
    #返回目前平台能识别的所有类别
    files = os.listdir(img_file_path.File_Train)
    print("class_getall:"+",".join(files))

    return render_template("class.html",classlist=files,object_map=Parameters.object_map)

#想某类别下添加照片
@app.route('/ai/class/img/add', methods=['POST'])
def img_add():

    class_name = request.form["class_name"]
    if(class_name==''):
        return httpResultWhiteMsg.send("必须选择上传类别")

    #分别获取post请求中的图片信息
    upload_files = request.files.getlist("imagefiles[]")
    if(len(upload_files)<10):
        return httpResultWhiteMsg.send("必须上传大于10张图片")
    #获取post请求中新增的类别名称

    class_path=img_file_path.File_Train+"\\"+class_name;
    test_path=img_file_path.File_Test+"\\"+class_name;
    print("class_name："+class_name)
    print("class_path："+class_path)
    if(os.path.exists(class_path)):
        return httpResultWhiteMsg.send("Class 已经存在")
    else:
        os.mkdir(class_path)
        os.mkdir(test_path)
        print("class_path："+class_path+" add success")

    #获取post请求中新增的类别中是测试数据还是训练数据、
    train_count=len(upload_files)/3
    img_count=1;
    for file in upload_files:
        if(img_count>train_count):
            file.save(os.path.join(class_path, str(img_count)+".jpg"))
        else:
            file.save(os.path.join(test_path, str(img_count)+".jpg"))
        img_count=img_count+1
    return httpResultWhiteMsg.send("上传成功！")


#想某类别下添加照片
@app.route('/ai/class/img/show', methods=['GET'])
def img_show():
    #获取post请求中新增的类别名称
    class_name = request.args.get('class_name')
    #返回这个类别下的所有图片：仅供展示
    file_path=img_file_path.File_Test+"\\"+class_name+"\\1.jpg";
    image = cv2.imread(file_path)
    return _serve_pil_image(file_path)



#重新训练AI
@app.route('/ai/train', methods=['GET'])
def ai_train():
    AiResNet50.train()
    return httpResultWhiteMsg.send("训练成功！")

@app.route('/img/fit', methods=['POST'])
def img_fit():
    #分别获取post请求中的图片信息
    upload_files = request.files['imagefile']
    #从post请求图片保存到本地路径中
    file = upload_files
    #随机生成uuid避免重复
    filename = uuid.uuid1()+".jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(image_path)
    result = AiResNet50Predict.predict(image_path)
    print(result)
    os.remove(image_path)
    return result

@auth.get_password
def get_password(username):
    if username == 'root':
        return 'root'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid data!'}), 400)

def _serve_pil_image(pil_img):
    return send_file(pil_img, mimetype='image/jpg', cache_timeout=0)

@app.before_request
def before_user():
    url = request.url
    print(url)
    in_pass=False
    for one_pass in pass_urls:
        if(one_pass in url):
            pass
            print("url in pass_urls")
            in_pass=True

    if(not in_pass):
        print("url not in pass_urls")
        if(session.get("user")==Parameters.user):
            print("session check pass")
            pass
        else:
            print("session check fail")
            return render_template("login.html")

if __name__ == '__main__':
    app.run(host=Parameters.host, port=Parameters.port)