from sanic import Sanic
from sanic.response import json,redirect
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
def query_string(request):
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })
    #如果请求的样子是?key1=value1&?key2=value2 request.args 会将它翻译成字典
if __name__ == '__main__':
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