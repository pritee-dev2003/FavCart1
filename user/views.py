from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
# Create your views here.

def index(request):
    user=request.session.get('userid')
    ct=""
    if user:
        ct=mcart.objects.all().filter(userid=user).count()
        request.session['cart']=ct
    x=category.objects.all().order_by("-id") #Filter(Name="Jenes",Cpic="")
    pdata=myproduct.objects.all().order_by("-id")
    a=myproduct.objects.all().filter(id=20)
    mydict={"data":x,"prodata":pdata,"p":a,"cart":ct}
    return render(request,'user/index.html',context=mydict)
###############################################
def about(request):
    user = request.session.get('userid')
    ct=""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
        request.session['cart'] = ct

    return render(request,'user/about.html',{"cart":ct})

def showcart(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
        request.session['cart'] = ct

    user=request.session.get('userid')
    a=request.GET.get('msg')
    cid=request.GET.get('cid')
    pid=request.GET.get('pid')
    if user:
      if a is not None:
        mcart.objects.all().filter(id=a).delete()
        return HttpResponse("<script>alert('Your item is deleted from Card');location.href='/user/showcart/'</script>")
      elif pid is not None:
          mcart.objects.all().filter(id=cid).delete()
          morder(userid=user,pid=pid,remark="pending",status=True,odate=datetime.now().date()).save()
          return HttpResponse("<script>alert('Your Order has been Placed successfully..');location.href='/user/myorder/'</script>")
    cursor=connection.cursor()
    cursor.execute("select p.*,c.* from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='"+str(user)+"'")
    cdata=cursor.fetchall()
    return render(request,'user/showcart.html',{"cart":ct,"cdata":cdata})

def cpdetail(request):
    c=request.GET.get('cid')
    p=myproduct.objects.all().filter(pcategory=c)
    return render(request,'user/cpdetail.html',{"pdata":p})
###############################################
def product(request):
    user = request.session.get('userid')
    ct=""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
        request.session['cart'] = ct

    return render(request,'user/product.html',{"cart":ct})
###############################################
def myorder(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
        request.session['cart'] = ct
    user=request.session.get('userid')
    pdata=""
    ddata=""
    oid=request.GET.get('oid')
    if user:
        if oid is not None:
           morder.objects.all().filter(id=oid).delete()
           return HttpResponse("<script>alert('Your Order has been cancelled... ');location.href='/user/myorder/'</script>")
        cursor=connection.cursor()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"' and o.remark='pending'")
        pdata=cursor.fetchall()
        cursor.execute("select p.*,o.* from user_myproduct p,user_morder o where p.id=o.pid and o.userid='" + str(user) + "' and o.remark='Delivered'")
        ddata = cursor.fetchall()
        #mydict={"odata":data}
    return render(request,'user/myorder.html',{"Cart":ct,"pdata":pdata,"ddata":ddata})
###############################################
def enquiry(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
        request.session['cart'] = ct
    status=False
    msg=""
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("email")
        c=request.POST.get("mob")
        d=request.POST.get("msg")
        contactus(Name=a,Email=b,Mobile=c,Message=d).save()
        status=True
        #mdict={"Name":a,"Email":b,"Mobile":c,"Message
        #msg={"m":status,"cart":ct}
    return render(request,'user/enquiry.html',{"m":status,"cart":ct})
###############################################
def signup(request):
    if request.method=="POST":
        Name=request.POST.get('name')
        Email=request.POST.get('email')
        Mobile=request.POST.get('mob')
        Passwd=request.POST.get('passwd')
        Address=request.POST.get('msg')
        Picture=request.FILES.get('pic')
        x=register.objects.all().filter(email=Email).count()
        if x==0:
            register(name=Name,email=Email,mobile=Mobile,ppic=Picture,passwd=Passwd,address=Address).save()
            return HttpResponse("<script>alert('You are registered successfully');location.href='/user/signup/'</script>")
        else:
            return HttpResponse("<script>alert('Your email id is already register..');location.href='/user/signup/'</script>")
    return render(request,'user/signup.html')
###############################################
def myprofile(request):
    user = request.session.get('userid')
    ct = ""
    if user:
        ct = mcart.objects.all().filter(userid=user).count()
    x=""
    if user:
        if request.method=="POST":
            Name=request.POST.get('name')
            Mobile=request.POST.get('mob')
            Passwd=request.POST.get('passwd')
            Address=request.POST.get('msg')
            Picture=request.FILES.get('pic')
            register(email=user,name=Name,mobile=Mobile,ppic=Picture,passwd=Passwd,address=Address).save()
            return HttpResponse("<script>alert('Your Profile Updated Successfully...');location.href='/user/profile/'</script>")
        x=register.objects.all().filter(email=user)
    return render(request,'user/myprofile.html',{"cart":ct,"mdata":x})
###############################################
def signin(request):
    if request.method=="POST":
        Email=request.POST.get('e')
        Passwd=request.POST.get('p')
        x=register.objects.all().filter(email=Email,passwd=Passwd).count()
        y = register.objects.all().filter(email=Email,passwd=Passwd)
        if x==1:
            request.session['userid']=Email
            request.session['userpic']=str(y[0].ppic)

            return HttpResponse("<script>alert('You are login successfully ');location.href='/user/index/'</script>")
        else:
            return HttpResponse("<script>alert('You are not login  ');location.href='/user/signin/'</script>")

    return render(request,'user/signin.html')
###############################################
def mens(request):
    cid=request.GET.get('msg')
    cat=category.objects.all().order_by('-id')
    d=myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=2, pcategory=cid)
    mydict={"cats":cat,"data":d,"a":cid}
    return render(request,'user/mens.html',mydict)
###############################################
def womens(request):
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid}

    return render(request,'user/womens.html',mydict)
###############################################
def kids(request):
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=4)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=4, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid}

    return render(request,'user/kids.html',mydict)
###############################################
def viewproduct(request):
    a=request.GET.get('abc')
    x=myproduct.objects.all().filter(id=a)
    return render(request,'user/viewproduct.html',{"pdata":x})
##############################################################
def signout(request):
    if request.session.get('userid'):
        del request.session['userid']
    return HttpResponse("<script>alert('You are signout...');location.href='/user/index/'</script>")
##################################################################
def myordr(request):
    user=request.session.get('userid')
    pid = request.GET.get('msg')
    if user:
        if pid is not None:
            morder(userid=user,pid=pid,remark="pending",odate=datetime.now().date(),status=True).save()
            return HttpResponse("<script>alert('Your order confirmed..');location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('You have login first...bbbbb');location.href='/user/signin/'</script>")
    return render(request,'user/myordr.html')
####################################
def mycart(request):
     p=request.GET.get('pid')
     user=request.session.get('userid')
     if user:
         if p is not None:
           mcart(userid=user,pid=p,cdate=datetime.now().date,status=True).save()
           return HttpResponse("<script>alert('you Item is added cart..');location.href='/user/index/'</script>")
     else:
           return HttpResponse("<script>alert('you have login first..');location.href='/user/signin/'</script>")
           return render(request,'user/mcart.html')