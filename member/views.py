# -*- coding: utf-8 -*-
import random
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context
from database.models import Activity , Code,Log,Section,User,UserTakePartInActivity
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage,InvalidPage
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import smtplib  
from email.mime.text import MIMEText  


mailto_list=["XXX@qq.com"] # 发送对象的列表
mail_host="smtp.qq.com"  #设置服务器
mail_user="754884172"    #用户名
mail_pass="XXXX"   #密码
mail_postfix="qq.com"  #发件箱的后缀

def send_mail(to_list,sub,content):  
    me="南微软"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False
# send_mail(mailto_list,"hello","hello world！")


def hello(request):
    return HttpResponse('hello world')
def home(request):
    return HttpResponse('this is home')
def reg(request):#注册
    reg=get_template('reg.html',)
    regHtml=reg.render(Context())
    return HttpResponse(regHtml)
def login(request):
	login=get_template('login.html')
	loginHtml=login.render(Context())
	return HttpResponse(loginHtml)

def index(request):# 显示自己的详细信息
    index=get_template('index.html')
    user=request.session.get('user')# 从session对象里面拿出user对象，session是运行这个网站时，每个页面
    if user is None: #都共有的一个公共对象，所以可以利用它来在各个页面之间传递参数之类
        return HttpResponse("请先登录！")# 如果session里面没有user对象，说明用户并没有登陆，所以返回错误页面
    #user = {'name': 'Sally', 'depart':'技术部','grade':'大一','college':'软件学园','major':'软件工程','phone':'15224652255','QQ':'7983452798'}
    
    indexHtml=index.render(Context({'user':user}))
    return HttpResponse(indexHtml)
def index_of_others(request,offset):# 显示别人的详细信息
    # offset是其他用户的name
    index=get_template('index_of_others.html')
    user=User.objects.get(name=offset)# 从数据库里查找所点击的用户
    u=request.session.get('user')# 没登陆的话报错
    if u is None:
        return HttpResponse("请先登录！")
    indexHtml=index.render(Context({'user':user}))
    return HttpResponse(indexHtml)
@csrf_exempt
def edit(request):
    edit=get_template('edit.html')
    user=request.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    editHtml=edit.render(Context({'user':user}))
    return HttpResponse(editHtml)
@csrf_exempt
def edit_result(request):# 编辑页面返回的结果
    sex= request.POST['sex']# 从前台的表单中拿回各种数据
    sec=request.POST['sec']
    college= request.POST['college']
    major= request.POST['major']
    grade= request.POST['grade']
    phone= request.POST['phone']
    qq= request.POST['qq']
    province= request.POST['province']
    city= request.POST['city']
    area= request.POST['area']
    campus= request.POST['campus']
    wechat= request.POST['wechat']
    love= request.POST['love']
    dormitory= request.POST['dormitory']
    u=request.session.get('user')
    email=u.email
    user=User.objects.get(email=email)#数据库里拿到所编辑的对象
    if user is None:
        return HttpResponse("请先登录！")
    
    user.sex=sex
    user.college=college
    user.major=major
    user.grade=grade
    user.phone=phone
    user.qq=qq
    user.province=province
    user.city=city
    user.area=area
    user.campus=campus
    user.wechat=wechat
    user.love=love
    user.dormitory=dormitory# 保存修改
    user.sec=Section.objects.get(id=sec)
    user.save()# 修改后的对象存入数据库
    request.session['user']=user# 用新的user替换掉之前旧的session里面的user对象
    return HttpResponseRedirect("/index")# 跳转到个人主页

def depart(request,offset):
	#depart=get_template('depart.html')
        user=request.session.get('user')
        if user is None:
            return HttpResponse("请先登录！")
	if offset=='all' :# 如果访问的网址是 depart/all的话，返回所有的用户信息
            userlst=User.objects.all()
            paginator = Paginator(userlst, 5) # 分页系统，每页显示5个用户
            try:
                page = int(request.GET.get('page', '1'))# 访问的网址是depart/all/page=?
            except ValueError: # 这里的page对象就是“？”后面的数字，用来标记访问的第几页
                page = 1# 出错的话直接访问第一页
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            user=request.session.get('user')
            #user.name='南微软'
            #user.depart='技术部'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'user':user,'contacts':contacts}));
            return HttpResponse(departHtml)
        if offset=='pre' or offset=='2':# 如果访问的是depart/pre或者 depart/2，显示主席团的成员信息
            userlst=User.objects.filter(sec=2)# 主席团的部门id是2，其他与上面相同
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':contacts,'user':user}));
            return HttpResponse(departHtml)
        if offset=='tech' or offset=='1':# 技术部
            userlst=User.objects.filter(sec=1)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':contacts,'user':user}));
            return HttpResponse(departHtml)
        if offset=='ope' or offset=='3': #运营部
            userlst=User.objects.filter(sec=3)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':contacts,'user':user}));
            return HttpResponse(departHtml)
        if offset=='adv' or offset=='4': #宣传
            userlst=User.objects.filter(sec=4)
            user=request.session.get('user')
            paginator = Paginator(userlst, 5)
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                contacts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                contacts = paginator.page(paginator.num_pages)
            #user.name='南微软'
            #user.depart='技术部'
            depart=get_template('depart.html')
            departHtml=depart.render(Context({'contacts':contacts,'user':user}));
            return HttpResponse(departHtml)
	# 查询数百具
	# 封装对象
	#departHtml=depart.render(Context());
	#return HttpResponse(departHtml)

@csrf_exempt
def reg_result(request): # 注册的结果页面
    password =  request.POST['password'] #从表单里拿到密码
    if password=='': # 没填密码
        return HttpResponse('注册失败！请填写密码')
    email =  request.POST['email']
    if email=='':# 没填邮箱
        return HttpResponse('注册失败！请填写邮箱')
    realname =  request.POST['realname']
    if realname=='':
        return HttpResponse('注册失败！请填写真实姓名')
    invitecode =  request.POST['invitecode']
    if invitecode=='':
        return HttpResponse('注册失败！请填写邀请码')
    u=User() # 新建一个User对象，把它存入数据库
    u.email=email
    u.password=hashlib.sha1(password).hexdigest() # 这是生成hash值代替明文的密码
    u.name=realname
    u.sec=Section.objects.get(id=1)
    u.save()
    request.session['user']=u # 把user对象放到session里面去
    result=get_template('result.html')
    resultHtml=result.render(Context())
    return HttpResponse(resultHtml)
@csrf_exempt
def login_result(request): # 登陆的结果
    password =  request.POST['password']
    if password=='':
        return HttpResponse('登陆失败！请填写密码')
    email =  request.POST['email']
    if email=='':
        return HttpResponse('登陆失败！请填写邮箱')
    u=User()
    u.email=email
    u.password=password
    try:
       user=User.objects.get(email=email) # user是指从数据库里面查找的邮箱为email的用户
    except User.DoesNotExist:
        return HttpResponse("账户不存在")
    if user.password==hashlib.sha1(u.password).hexdigest(): # u是登陆之时填写的用户
        result=get_template('login_result.html') # 比较数据库的用户的密码和填写的密码是否一致
        resultHtml=result.render(Context())
        request.session['user']=user
        return HttpResponse(resultHtml)
    else:
        return HttpResponse("密码错误")
    

def get_paginator(obj,page): # 这个函数不用管它
    page_size = 10 #每页显示的数量
    after_range_num = 5
    before_range_num = 6 
    context = {}
    try:
        page = int(page)
        if page <1 :
            page = 1 
    except ValueError:
        page = 1 
    paginator = Paginator(obj,page_size)
    try:
        obj = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        obj = paginator.page(1)
    
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+before_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+before_range_num]
    
    context["page_objects"]=obj
    context["page_range"]=page_range
    return context
def logout(requst):# 注销，从session里面删除user对象，并跳转回登陆页面
    user=requst.session.get('user')
    if user is None:
        return HttpResponse("请先登录！")
    del requst.session['user']
    return HttpResponseRedirect("/login")
def getstr(n):#获得指定长度随机字符串
    st = ''
    while len(st) < n:
        temp = chr(97+random.randint(0,25))
        if st.find(temp) == -1 :
            st = st.join(['',temp])
    return st

    
