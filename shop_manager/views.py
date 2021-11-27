from django.shortcuts import render
import mysql.connector as sq
import datetime
import re
def home(request):
    return render(request,"home.html")
def customer_info(request):
    return render(request,"customer_info.html")
def inventory1(request):
    return render(request,"inventory1.html")
def inventory2(request):
    return render(request,"inventory2.html")
def item_detail1(request):
    d=request.POST
    con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
    cur=con.cursor()
    code=d["code"]
    stmt="select * from item_details where CODE={}".format(code)
    cur.execute(stmt)
    l=cur.fetchone()
    item_detailhtml(l)
    return render(request,"item_detail1.html")
def item_detailhtml(l):
    f=open("C://Users//ADMIN//Desktop//ananya//Scripts//shop_manager//shop_manager//templates//item_detail1.html","w")
    s="""<html><body bgcolor="pink">
    <p>HOME PAGE::<a href="http://localhost:8000/home/">  CLICK HERE! </a></p>
    <center>
    <font size=6 color="green">CODE: {}
    <br>
    <br>
    CATEGORY:  {}
    <br>
    <br>
    ITEM_NAME:  {}
    <br>
    <br>
    QUANTITY_AVAILABLE:  {}
    <br>
    <br>
    UNIT:  {}
    <br>
    <br>
    MRP:  {}
    <br>
    <br>
    GST:  {}
    <br>
    <br>
    DISCOUNT:  {}
    </center>""".format(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7])
    f.write(s)
    f.close()
phno=""
t=''
def bill(request):
    global phno
    global t
    if request.method=="POST":
        d=request.POST
        con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
        cur=con.cursor()
        phno=d["contact_no"]
        stmt="insert into customer_details values('{}','{}','{}','{}');".format(d["cust_name"],d["contact_no"],d["address"],d["email_id"])
        cur.execute(stmt)
        con.commit()
        t=re.sub('[^A-Za-z0-9]+', '', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        stmt="create table bill{}(CODE int, ITEM_NAME varchar(50), QUANTITY float, PRICEperUNIT float, GST_percent int, GSTperUNIT float, NET_GST float, NET_PRICEperUNIT float, TOTAL_PRICE float);".format(t)
        cur.execute(stmt)
        con.commit()
    if request.method=="GET":
        code=request.GET.get('code')
        qty=request.GET.get('quantity')
        con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
        cur=con.cursor()
        stmt="select ITEM_NAME,QUANTITY_AVAILABLE,MRP,GST,DISCOUNT from item_details where CODE={};".format(code)
        cur.execute(stmt)
        a,b,c,d,e=cur.fetchone()
        price=c/(1+(0.01*d))
        disc_price=price*(1-(0.01*e))
        gst=disc_price*0.01*d
        net_price=disc_price+gst
        tot_price=net_price*int(qty)
        netgst=int(qty)*gst
        stmt="update item_details set QUANTITY_AVAILABLE=QUANTITY_AVAILABLE-{} where CODE={};".format(qty,code)
        cur.execute(stmt)
        con.commit()
        stmt="insert into bill{} values({},'{}',{},{},{},{},{},{},{});".format(t,code,a,qty,disc_price,d,gst,netgst,net_price,tot_price)
        cur.execute(stmt)
        con.commit()
    return render(request,"bill.html")
def html_table1(l,m):
    f=open("C://Users//ADMIN//Desktop//ananya//Scripts//shop_manager//shop_manager//templates//bill_receipt.html","w")
    s="""<html><body bgcolor="pink">
    <p>HOME PAGE::<a href="http://localhost:8000/home/">  CLICK HERE! </a></p>
    <font size=5 color="green">CUSTOMER NAME: {}
    <br>
    CONTACT NO: {}
    <br>
    </font>
    <table border=1 frame=hsides rules=all style="width:100%">
    <font size="36" color="red"><center>BILL</center></font>
    <br>
    <br>
    <br>
    <font size="15" color="green">
    <tr>
    <th>ITEM CODE</th>
    <th>ITEM NAME</th>
    <th>QUANTITY</th>
    <th>PRICE PER UNIT</th>
    <th>GST PERCENT</th>
    <th>GST PER UNIT</th>
    <th>NET GST</th>
    <th>NET PRICE PER UNIT</th>
    <th>TOTAL PRICE</th>""".format(m[0],m[1])
    count=0
    for i in l:
        s+="""<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>""".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
        count+=i[7]
    s+="""<td colspan="8"><center>GRAND TOTAL</center></td>
    <td>{}</td></table></font></body></html>""".format(count)
    f.write(s)
    f.flush()
def bill_receipt(request):
    if request.method=="GET":
        code=request.GET.get('code')
        qty=request.GET.get('quantity')
        con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
        cur=con.cursor()
        stmt="select ITEM_NAME,QUANTITY_AVAILABLE,MRP,GST,DISCOUNT from item_details where CODE={};".format(code)
        cur.execute(stmt)
        a,b,c,d,e=cur.fetchone()
        price=c/(1+(0.01*d))
        disc_price=price*(1-(0.01*e))
        gst=disc_price*0.01*d
        net_price=disc_price+gst
        tot_price=net_price*int(qty)
        netgst=int(qty)*gst
        stmt="update item_details set QUANTITY_AVAILABLE=QUANTITY_AVAILABLE-{} where CODE={};".format(qty,code)
        cur.execute(stmt)
        con.commit()
        stmt="insert into bill{} values({},'{}',{},{},{},{},{},{},{});".format(t,code,a,qty,disc_price,d,gst,netgst,net_price,tot_price)
        cur.execute(stmt)
        con.commit()
        stmt="select * from bill{};".format(t)
        cur.execute(stmt)
        x=cur.fetchall()
        stmt="select Customer_name,Contact_no from customer_details where Contact_no='{}';".format(phno)
        cur.execute(stmt)
        y=cur.fetchone()
        html_table1(x,y)
    return render(request,"bill_receipt.html")
def showbill(request):
    con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
    cur=con.cursor()
    stmt="show tables;"
    cur.execute(stmt)
    bills=cur.fetchall()
    bills=bills[:-3]
    f=open("C://Users//ADMIN//Desktop//ananya//Scripts//shop_manager//shop_manager//templates//showbill.html","w")
    s='''<p>HOME PAGE::<a href="http://localhost:8000/home/">  CLICK HERE! </a></p>
    <body bgcolor="pink">
    <table border=1 frame=hsides rules=all style="width:100%">
    <font size="100" color="blue"><center>ALL BILLS</center></font>
    <br>
    <br>
    <br>
    <br>
    <br>
    <tr>
    <th>S NO.</th>
    <th>BILL</th>'''
    sno=1
    for i in bills:
        s+="""<tr>
        <td align="center">{}</td>
        <td align="center">{}</td>
        </tr>""".format(sno,i)
        sno+=1
    s+="""<td colspan="7"></table></font></body></html>"""
    f.write(s)
    f.flush()
    return render(request,"showbill.html")
def salesgst(request):
    return render(request,"sales&gst.html")
def daterange(start,end):
    start=start[:4]+"-"+start[4:6]+"-"+start[-2:]
    end=end[:4]+"-"+end[4:6]+"-"+end[-2:]
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_array = \
    (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
    l=[]
    for date_object in date_array:
        l.append(date_object.strftime("%Y-%m-%d"))
    return l
def dailysale(request):
    x=daterange('20191203',re.sub('[^A-Za-z0-9]+', '',datetime.datetime.now().strftime("%Y-%m-%d")))
    con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
    cur=con.cursor()
    stmt="show tables;"
    cur.execute(stmt)
    tables=cur.fetchall()
    tables=tables[:-3]
    dict={}
    for i in tables:
        stmt="select sum(TOTAL_PRICE) from {};".format(i[0])
        cur.execute(stmt)
        t=cur.fetchone()
        dict[i]=int(t[0])
    print(dict)
    dict2={}
    for i in range(len(x)):
        x[i]=re.sub('[^A-Za-z0-9]+', '',x[i])
    for i in x:
        for j in dict:
            if i==j[0][4:12]:
                if i in dict2:
                    dict2[i]+=dict[j]
                else:
                    dict2[i]=dict[j]
    print(dict2)
    dict3={}
    for i in dict2:
        dict3[dateconvert(i)]=dict2[i]
    htmltable3(dict3)
    return render(request,"dailysale.html")
def gstdict(request):
    x=daterange('20191203',re.sub('[^A-Za-z0-9]+', '',datetime.datetime.now().strftime("%Y-%m-%d")))
    con=sq.connect(host="localhost",user="root",password="ananya1802",database="shop_manager")
    cur=con.cursor()
    stmt="show tables;"
    cur.execute(stmt)
    tables=cur.fetchall()
    tables=tables[:-3]
    dict={}
    for i in tables:
        stmt="select sum(NET_GST) from {};".format(i[0])
        cur.execute(stmt)
        t=cur.fetchone()
        dict[i]=int(t[0])
    dict2={}
    for i in range(len(x)):
        x[i]=re.sub('[^A-Za-z0-9]+', '',x[i])
    for i in x:
        for j in dict:
            if i==j[0][4:12]:
                if i in dict2:
                    dict2[i]+=dict[j]
                else:
                    dict2[i]=dict[j]
    dict3={}
    for i in dict2:
        dict3[dateconvert(i)]=dict2[i]
    htmltable2(dict3)
    return render(request,"gstcollect.html")
def htmltable2(d):
    f=open("C://Users//ADMIN//Desktop//ananya//Scripts//shop_manager//shop_manager//templates//gstcollect.html","w")
    s="""<html><body bgcolor="pink">
    <p>HOME PAGE::<a href="http://localhost:8000/home/">  CLICK HERE! </a></p>
    <table border=5 frame=hsides rules=all style="width:100%">
    <font size="80" color="brown"><center>GST COLLECTION</center></font>
    <br>
    <br>
    <br>
    <tr>
    <th>DATE</th>
    <th>GST COLLECTED</th>"""
    for i in d:
        s+="""<tr>
        <td align="center">{}</td>
        <td align="center">{}</td>
        </tr>""".format(i,d[i])
    f.write(s)
    f.flush()
def htmltable3(d):
    f=open("C://Users//ADMIN//Desktop//ananya//Scripts//shop_manager//shop_manager//templates//dailysale.html","w")
    s="""<html><body bgcolor="pink">
    <p>HOME PAGE::<a href="http://localhost:8000/home/">  CLICK HERE! </a></p>
    <table border=5 frame=hsides rules=all style="width:100%">
    <font size="80" color="brown"><center>DAILY SALE</center></font>
    <br>
    <br>
    <br>
    <tr>
    <th>DATE</th>
    <th>SALE</th>"""
    for i in d:
        s+="""<tr>
        <td align="center">{}</td>
        <td align="center">{}</td>
        </tr>""".format(i,d[i])
    f.write(s)
    f.flush()
def dateconvert(x):
    months={'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
    y='{} {} {}'.format(x[-2:],months[x[-4:-2]],x[:4])
    return y
