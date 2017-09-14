from sanic import Blueprint
from sanic.exceptions import NotFound
from sanic.response import json,text
bp = Blueprint('my_blueprint')

@bp.route('/hehe/lalala')
async def lalala(request):
    return text('我靠')
@bp.middleware('request')
async def print_lol(request):
    print('蓝图的中间件是对全局影响的')

@bp.exception(NotFound)
def ignore_404s(request, exception):
    return text("bp:Yep, I totally found the page: {}".format(request.url))