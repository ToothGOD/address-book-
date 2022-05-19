import tkinter.messagebox
import tkinter as tk
import sqlite3
class LoginPage:                                                                                        #登陆界面
    def __init__(self, root):                                                                           #登陆GUI界面编写
        self.win = root
        self.win.geometry('210x80')
        self.win.title('通讯录')
        self.page = tk.Frame(win)
        self.page.pack()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        tk.Label(self.page, text='账户').grid(row=1, column=0)                                           #提示用户
        tk.Entry(self.page, textvariable=self.username, width=15).grid(row=1, column=1)                 #用户输入框
        tk.Label(self.page, text='密码').grid(row=2, column=0)                                           #提示密码
        tk.Entry(self.page, textvariable=self.password, width=15).grid(row=2, column=1)                 #密码输入框
        tk.Button(self.page, text='登 陆', command=self.login, width=12).grid(row=3, column=0)           #点击登陆进行登陆操作
        tk.Button(self.page, text='注 册', command=self.register, width=12).grid(row=3, column=1)        #点击注册进行注册操作
    def login(self):                                                                                    #登陆操作
        global data                                                                                     #将data定义为全局变量
        data = 'data_' + '%s' % (self.username.get())
        conn = sqlite3.connect("D:\\data.db")
        cur = conn.cursor()
        cur.execute("select * from login where username='{}'".format(self.username.get()))
        conn.commit()
        for row in cur:                                                                                 #验证密码
            if self.username.get() == row[0] and self.password.get() == row[1]:
                self.page.destroy()
                Find(self.win)                                                                          #跳转到查询页面
            else:
                tk.messagebox.showwarning(title='错误', message='密码错误')                               #密码不匹配提示密码错误
        cur.close()
        conn.close()
    def register(self):                                                                                 #跳转至注册界面
        self.page.destroy()
        RegisterPage(self.win)
class RegisterPage:                                                                                     #注册界面
    def __init__(self, root):                                                                           #注册GUI界面编写
        self.win = root
        self.win.geometry('210x80')
        self.win.title('通讯录管理系统')
        self.page = tk.Frame(win)
        self.page.pack()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        tk.Label(self.page, text='账户').grid(row=1, column=0)  # 提示用户
        tk.Entry(self.page, width=15, textvariable=self.username).grid(row=1, column=1)  # 用户输入框
        tk.Label(self.page, text='密码').grid(row=2, column=0)  # 提示密码
        tk.Entry(self.page, width=15, textvariable=self.password).grid(row=2, column=1)
        tk.Button(self.page, text='注册', width=15, command=self.addlogindb).grid(row=3, column=1)
    def addlogindb(self):                                                                                  #添加用户信息
        global data                                                                                        #将data定义为全局变量
        data = 'data_' + '%s' % (self.username.get())
        conn = sqlite3.connect("D:\\data.db")
        conn.execute("create table if not exists login(username varchar(128) primary key,password varchar(128));")                                                                             #创建登录信息表
        conn.execute("create table if not exists '{}'(UID varchar(128) primary key,phone varchar(128), QQ varchar(128),address varchar(125));" .format('data_'+self.username.get()))        #创建用户存储信息表
        conn.execute("insert or ignore into login(username, password)values ('{}','{}')".format(self.username.get(), self.password.get()))                                               #将账户信息添加至登录信息表
        conn.commit()
        conn.close()
        self.page.destroy()
        Find(self.win)                                                                                     #跳转至查询页面
class Find:                                                                                                #查询界面
    def __init__(self,root):                                                                               #查询GUI界面编写
        self.win = root
        self.win.geometry('400x200')
        self.win.title('通讯录')
        self.page = tk.Frame(win)
        self.page.pack()
        self.uid = tk.StringVar()
        tk.Label(self.page, text='输入姓名以查询联系人').grid(row=1, column=0)
        tk.Label(self.page, text='姓名').grid(row=2, column=0)
        tk.Entry(self.page, textvariable=self.uid, width=15).grid(row=2, column=1)
        tk.Label(self.page, text='电话').grid(row=3, column=0)
        tk.Label(self.page, text='QQ').grid(row=4, column=0)
        tk.Label(self.page, text='地址').grid(row=5, column=0)
        tk.Button(self.page, text='查询', width=12, command=self.finding).grid(row=6, column=0)
        menubar = tk.Menu(self.win)
        menubar.add_command(label='查询')
        menubar.add_command(label='修改', command=self.changepage)
        menubar.add_command(label='添加', command=self.addpage)
        menubar.add_command(label='删除', command=self.delpage)
        self.win['menu'] = menubar
    def finding(self):                                                                                     #查找操作
        conn = sqlite3.connect("D:\\data.db")
        cur = conn.cursor()
        cur.execute("select * from '{}' where UID='{}'".format(data, self.uid.get()))
        conn.commit()
        for row in cur:
            tk.Label(self.page, text='' + row[1] + '').grid(row=3, column=1)
            tk.Label(self.page, text='' + row[2] + '').grid(row=4, column=1)
            tk.Label(self.page, text='' + row[3] + '').grid(row=5, column=1)
        cur.close()
        conn.close()
    def changepage(self):                                                                                   #跳转修改页面
        self.page.destroy()
        Change(self.win)
    def addpage(self):                                                                                      #跳转添加界面
        self.page.destroy()
        Add(self.win)
    def delpage(self):                                                                                      #跳转删除界面
        self.page.destroy()
        Del(self.win)
class Change:                                                                                               #修改界面
    def __init__(self, root):                                                                               #修改GUI界面编写
        self.win = root
        self.win.geometry('400x200')
        self.win.title('通讯录')
        self.page = tk.Frame(win)
        self.page.pack()
        self.uid = tk.StringVar()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.qq = tk.StringVar()
        self.address = tk.StringVar()
        tk.Label(self.page, text='输入姓名以修改联系人').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.uid, width=15).grid(row=1, column=2)
        tk.Label(self.page, text='姓名').grid(row=2, column=0)
        tk.Entry(self.page, textvariable=self.name, width=15).grid(row=2, column=2)
        tk.Label(self.page, text='电话').grid(row=3, column=0)
        tk.Entry(self.page, textvariable=self.phone, width=15).grid(row=3, column=2)
        tk.Label(self.page, text='QQ').grid(row=4, column=0)
        tk.Entry(self.page, textvariable=self.qq, width=15).grid(row=4, column=2)
        tk.Label(self.page, text='地址').grid(row=5, column=0)
        tk.Entry(self.page, textvariable=self.address, width=15).grid(row=5, column=2)
        tk.Button(self.page, text='查询', width=12, command=self.finding).grid(row=6, column=0)
        tk.Button(self.page, text='修改', width=12, command=self.changeing).grid(row=6, column=2)
        menubar = tk.Menu(self.win)
        menubar.add_command(label='查询', command=self.findpage)
        menubar.add_command(label='修改')
        menubar.add_command(label='添加', command=self.addpage)
        menubar.add_command(label='删除', command=self.delpage)
        self.win['menu'] = menubar
    def finding(self):                                                                                      #查找操作
        conn = sqlite3.connect("D:\\data.db")
        cur = conn.cursor()
        cur.execute("select * from '{}' where UID='{}'".format(data, self.uid.get()))
        conn.commit()
        for row in cur:
            tk.Label(self.page, text='' + row[0] + '', width=15).grid(row=2, column=1)
            tk.Label(self.page, text='' + row[1] + '', width=15).grid(row=3, column=1)
            tk.Label(self.page, text='' + row[2] + '', width=15).grid(row=4, column=1)
            tk.Label(self.page, text='' + row[3] + '', width=15).grid(row=5, column=1)
        cur.close()
        conn.close()
    def changeing(self):                                                                                    #修改操作
        conn = sqlite3.connect("D:\\data.db")
        conn.execute("update '{}' set UID='{}',phone='{}', qq='{}',address='{}' where UID='{}'".format(data, self.name.get(), self.phone.get(), self.qq.get(), self.address.get(), self.uid.get()))
        conn.commit()
        conn.close()
        self.page.destroy()
        Change(self.win)
        tk.messagebox.showwarning(title='提示', message='修改成功')
    def findpage(self):                                                                                     #跳转查询界面
        self.page.destroy()
        Find(self.win)
    def addpage(self):                                                                                      #跳转添加界面
        self.page.destroy()
        Add(self.win)
    def delpage(self):                                                                                      #跳转删除界面
        self.page.destroy()
        Del(self.win)
class Add:                                                                                                  #添加界面
    def __init__(self, root):                                                                               #添加GUI界面编写
        self.win = root
        self.win.geometry('400x200')
        self.win.title('通讯录')
        self.page = tk.Frame(win)
        self.page.pack()
        self.name = tk.StringVar()
        self.phone = tk.StringVar()
        self.qq = tk.StringVar()
        self.address = tk.StringVar()
        tk.Label(self.page, text='姓名').grid(row=2, column=0)
        tk.Entry(self.page, textvariable=self.name, width=15).grid(row=2, column=1)
        tk.Label(self.page, text='电话').grid(row=3, column=0)
        tk.Entry(self.page, textvariable=self.phone, width=15).grid(row=3, column=1)
        tk.Label(self.page, text='QQ').grid(row=4, column=0)
        tk.Entry(self.page, textvariable=self.qq, width=15).grid(row=4, column=1)
        tk.Label(self.page, text='地址').grid(row=5, column=0)
        tk.Entry(self.page, textvariable=self.address, width=15).grid(row=5, column=1)
        tk.Button(self.page, text='储存', command=self.adding, width=14).grid(row=6, column=1)
        menubar = tk.Menu(self.win)
        menubar.add_command(label='查询', command=self.findpage)
        menubar.add_command(label='修改', command=self.changepage)
        menubar.add_command(label='添加')
        menubar.add_command(label='删除', command=self.delpage)
        self.win['menu'] = menubar
    def adding(self):                                                                                       #添加操作
        conn = sqlite3.connect("D:\\data.db")
        conn.execute("insert into '{}'(UID, phone,QQ,address)values ('{}','{}','{}','{}')".format(data,self.name.get(), self.phone.get(), self.qq.get(), self.address.get()))
        conn.commit()
        conn.close()
        self.page.destroy()
        Add(self.win)
        tk.messagebox.showwarning(title='提示', message='添加成功')
    def findpage(self):                                                                                      #跳转查询界面
        self.page.destroy()
        Find(self.win)
    def changepage(self):                                                                                    #跳转修改界面
        self.page.destroy()
        Change(self.win)
    def delpage(self):                                                                                       #跳转删除界面
        self.page.destroy()
        Del(self.win)
class Del:                                                                                                   #删除界面
    def __init__(self, root):                                                                                #删除GUI界面编写
        self.win = root
        self.win.geometry('400x200')
        self.win.title('通讯录')
        self.page = tk.Frame(win)
        self.page.pack()
        self.uid = tk.StringVar()
        tk.Label(self.page, text='输入姓名以删除联系人').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.uid, width=15).grid(row=1, column=1)
        tk.Label(self.page, text='姓名').grid(row=2, column=0)
        tk.Label(self.page, text='电话').grid(row=3, column=0)
        tk.Label(self.page, text='QQ').grid(row=4, column=0)
        tk.Label(self.page, text='地址').grid(row=5, column=0)
        tk.Button(self.page, text='查询', width=12, command=self.finding).grid(row=6, column=0)
        tk.Button(self.page, text='删除', width=12, command=self.deling).grid(row=6, column=1)
        menubar = tk.Menu(self.win)
        menubar.add_command(label='查询', command=self.findpage)
        menubar.add_command(label='修改',command=self.changepage)
        menubar.add_command(label='添加', command=self.addpage)
        menubar.add_command(label='删除')
        self.win['menu'] = menubar
    def finding(self):                                                                                      #查询操作
        conn = sqlite3.connect("D:\\data.db")
        cur = conn.cursor()
        cur.execute("select * from '{}' where UID='{}'".format(data, self.uid.get()))
        conn.commit()
        for row in cur:
            tk.Label(self.page, text='' + row[0] + '', width=15).grid(row=2, column=1)
            tk.Label(self.page, text='' + row[1] + '', width=15).grid(row=3, column=1)
            tk.Label(self.page, text='' + row[2] + '', width=15).grid(row=4, column=1)
            tk.Label(self.page, text='' + row[3] + '', width=15).grid(row=5, column=1)
        cur.close()
        conn.close()
    def deling(self):                                                                                       #删除操作
        conn = sqlite3.connect("D:\\data.db")
        conn.execute("delete from '{}' where UID ='{}'".format(data, self.uid.get()))
        conn.commit()
        conn.close()
        self.page.destroy()
        Del(self.win)
        tk.messagebox.showwarning(title='提示', message='删除成功')
    def findpage(self):                                                                                     #跳转查询界面
        self.page.destroy()
        Find(self.win)
    def changepage(self):                                                                                   #跳转修改界面
        self.page.destroy()
        Change(self.win)
    def addpage(self):                                                                                      #跳转添加界面
        self.page.destroy()
        Add(self.win)
if __name__ == '__main__':
    win = tk.Tk()
    LoginPage(root=win)
    win.mainloop()


