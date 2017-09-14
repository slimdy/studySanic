from sanic import Sanic
from sanic.response import json,redirect,text
from sanic.exceptions import abort,ServerError,SanicException,NotFound
from myBlueprint import bp

app = Sanic(__name__)
app.static('/static','./static')
app.static('/the_best.jpeg','/Users/slimdy/Desktop/ID2.jpeg')
@app.route('/',methods=['GET'],host='localhost:8000')#默认接收get
async def hello(request): #一定要加async
    return json({"hello":request.query_string})

@app.route('/',methods=['GET'])#如果访问者的访问的域名不是host的内容，则使用下面的这个同名方法
async def hello(request):
    return json({'fuck':'off','name':request.query_string})

@app.get("/json")#可以简写成这样，他们的原型是app.add_route(post_json,'/json')
async def get_json(request):
    print(request.ip)#接收ip
    # if request.app.config['DEBUG']: #可以获得app的一些属性
    #     return json({ "received": True, "message": request.json })#请求体是json的话会输出
    # else:
    return 'fuck off'

@app.get("/hello")
async def go_hello(request):
    url = app.url_for('query_string',id=123,name='slimdy',_anchor='slim',_external=True)
    #url_for 还有几个参数
    #_anchor='slimdy' 在url尾部添加#slimdy
    # _extenrnal = True 这个参数必须与_server 或者 _scheme 一起用 否则和没设置一样
    #_server = 'localhost:8000' 会在url的头部添加服务器名
    #_scheme = 'http'  会在url的头部添加协议名称
    print(url)
    return redirect(url)

@app.route("/form")
async def get_json(request):
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })

@app.route("/files")
async def post_json(request):
    test_file = request.files.get('test')

    file_parameters = {
        'body': test_file.body,
        'name': test_file.name,
        'type': test_file.type,
    }
    return json({ "received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters })

@app.route("/query_string")
async def query_string(request):
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })
    #如果请求的样子是?key1=value1&?key2=value2 request.args 会将它翻译成字典
@app.route('/killme')
def  i_am_ready_to_dead(request):
    raise ServerError('something bad happened',status_code=500)
@app.route('/no_no')
def  nono(request):
    abort(400)
    text('fuck off')#这句是不会执行的
# @app.exception([ServerError,SanicException,NotFound])
# def handle_exception(request,exception):
#     return text('Yep,I totally found the page:{}'.format(request.url))

# @app.middleware('request')
# async def print_request(resquest):
#     print('I print when a request is received by the server')
# @app.middleware('response')
# async def print_response(request,response):
#     response.headers['Server'] = 'Fake-Server'
#     response.headers['x-xss-protection'] = '1;mode=block'
#     print('I pirnt when a response is returned by the server')
# async def print_response(request,response):
#     return text('haha')#如果在中间件中返回，则请求直接就被返回
@app.listener('before_server_start')
async def say_hello(app,loop):
    print('welcome run server')
async def say_OK():
    print('start server successfully!')
if __name__ == '__main__':
    app.add_task(say_OK())
    app.blueprint(bp)
    app.run(host='0.0.0.0',port=8000,debug=True)


"""
request :
request.json: 请求体重有json事可以用 直接得到json 数据
request.args: 如果请求的样子是?key1=value1&?key2=value2 request.args 会将它翻译成字典
request.files.get(name).body ,.name,.type
request.form :获得表单数据
request。body 获得请求体
request.ip 获得访问者ip
request.app.config 获得访问者访问的app的配置
``.url 请求的url
``.scheme 请求的协议
``.host 请求的主机
``.path 请求的路径
``.query_string 请求的的这个字符串
"""
'''
RequestParameters 是 sanic.request 提供的一个 request参数类
可以通过get(name,default=none) 或者 getlist(name,default=none) 他们的区别是 如果参数是个list 则get 只能获得第一个值
'''

"""
response:
``.text('txt')  返回文本
``.html('html') 返回html
``.json(dict) 返回json 里面用字典
``.file('scr/img.jpg') 返回资源
``.Streaming(streamingFunction,content_type='text/plain') 返回二进制流，第一个参数是生成二进制流的方法，第二个是什么类型的二进制流
``.file_streaming('scr/img.jpg') 返回文件的二进制流
``.redirect(url) 跳转url  状态码是302
``.raw('raw data') 返回不加工的数据
return response.json( 以上每个方法，都可以添加请求头和状态码
        {'message': 'Hello world!'},
        headers={'X-Served-By': 'sanic'},
        status=200
    )
"""

"""
静态文件
设置静态文件或文件夹
app.static('/static','./static') 这个是设置静态文件夹  如果url里有/static 就去 ./static里面找去  
app.static('/the_best.png','/home/slimdy/images/hehe.png')  如果请求thebest.png 就返回hehe.png
可以使用url_for () 来创建静态文件的地址 还不知道怎么用
"""

"""
异常处理
抛出异常
raise ServerError (message,status_code)
abort(status_code,message)
可以用装饰器@app.exception(list exception) 底下定义函数用来处理捕捉到异常应该如何处理，参数要带request，和exception
"""

"""
中间件
可以利用中间件 在接受请求时，和发送响应时，做出修改
@app.middleware('request')或者@app.middleware('response')
得到response 和request 可以修改header，cookies等信息
监听者
如果需要在Server开启或者结束时触发使用
@app.listener('before_server_start') 他装饰的方法 有两个参数app，和loop
before_server_start
after_server_start
before_server_stop
after_server_stop

还有一种方法可以在loop启动以后，给队列添加任务app.add_task(function())
"""

"""
蓝图
有了蓝图的出现，终于不必把所有的处理请求方法卸载一个文件里了
重新定义一个文件名叫myBluePrint.py
在里面生成蓝图对象
然后这个蓝图对象可以代替原来的@app
但是要知道，必须在启动文件里注册一下 app.blueprint(name)
蓝图的中间件，异常都和 app的实例一样 影响全局
蓝图的定义，可以给这个蓝图内的路由添加url_prefix 
blueprint_v1 = Blueprint('v1', url_prefix='/v1') 在定义的时候
app.blueprint(blueprint_v1, url_prefix='/v1') 再注册的时候
最后 不要忘了在蓝图中使用url_for的时候，如果有前缀，需要在第一个参数加上前缀

"""

"""
配置
基本的配置方法
app.config.DB_NAME = ''
也可以放在字典里 一次性更新
db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}
app.config.update(db_settings)
从对象中加载配置
import myapp.default_settings
app = Sanic('myapp')
app.config.from_object(myapp.default_settings)
从文件中加载
app.config.from_pyfile('/path/to/configuration')文件里的配置名称都要大写
上面的这个换一种写法
app.config.from_envvar('MYAPP_SETTINGS')
这种写法，在启动项目的时候$ MYAPP_SETTINGS=/path/to/config_file python3 myapp.py
"""

"""
cookies 
读取
@app.route("/cookie")
async def test(request):
    test_cookie = request.cookies.get('test')
    return text("Test cookie set to: {}".format(test_cookie))

写入
from sanic.response import text
@app.route("/cookie")
async def test(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response

删除
from sanic.response import text

@app.route("/cookie")
async def test(request):
    response = text("Time to eat some cookies muahaha")
    # 这个cookie的过期时间将被设置为0
    del response.cookies['kill_me']

    # 这个cookie 5 秒后自毁
    response.cookies['short_life'] = 'Glad to be here'
    response.cookies['short_life']['max-age'] = 5
    del response.cookies['favorite_color']

    # 这个cookie 将保留为改变的状态
    response.cookies['favorite_color'] = 'blue'
    response.cookies['favorite_color'] = 'pink'
    del response.cookies['favorite_color']
    return response
    
响应的cookie 还有很多的东西能够设置：
expires (datetime): 在客户端浏览器过期时间.
path (string): cookie 所来的路径  默认是/
comment (string): 注释'
domain (string): 定义这个cookie 在哪个域名下是合法的，明确定义域名前面必须要加. 例如.sanic.readthedocs.io
max-age (number): cookie 存活的最大秒数.
secure (boolean): 定义cookie是否只能通过https 发送.
httponly (boolean): 定义cookie 能不能被js读取和修改
"""
#下次学的时候不要忘了 看一下asycn 和await 是什么鬼
