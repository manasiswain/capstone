from flask import Flask,render_template,request,flash,redirect, url_for
import os
import shutil
from werkzeug.utils import secure_filename
import nltk
import pandas as pd
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import requests
import ast
#global
import psycopg2

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

con = psycopg2.connect(
            host = "127.0.0.1",
            database="postgres",
            user = "postgres",
            password = "postgres",
            port="5431")
detected = []
l=[]
rl=[]
lit=[]
d_lst={}
d_cal = {}
st=""
recom=[]
email=""
category=""
'''cur = con.cursor()
postgreSQL_se_Query = "SELECT rec from users"
cur.execute(postgreSQL_se_Query)
rows = cur.fetchall()
cur.close()
for i in rows:
    recom.append(i)'''
basicingredients=['salt','sugar', 'pepper', 'oil', 'water', 'clove', 'cumin', 'cardamom', 'cinnamon', 'turmeric', 'powder',
             'masala', 'anise', 'corriander', 'basil', 'mustard', 'oregano']
super_basic = ['oil', 'sugar']
sb=[]
datasets = ['indian', 'dessert', 'diabetic','side_dish', 'salad', 'gluten_free','keto', 'low_carb', 'mocktail','smoothie']
app=Flask(__name__)
app.config['SECRET_KEY'] = 'breakdown'
def api(x):
    query = x
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'AoDDjsJQhDiBLBpoL8hslg==kjKefEQOCD894gSI'})
    if response.status_code == requests.codes.ok:
        s = response.text
        s = s[1:-1]
        res = ast.literal_eval(s)
        return(res['calories'])
    else:
        return("N")
def recommend_recipe(df_input,mapping,similarity_matrix,df):
    df_index = mapping[df_input]
    similarity_score = list(enumerate(similarity_matrix[df_index]))
    #sort in descending order the similarity score of movie inputted with all the other movies
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    # Get the scores of the 15 most similar movies. Ignore the first movie.
    similarity_score = similarity_score[1:15]
    #return movie names using the mapping series
    df_indices = [i[0] for i in similarity_score]
    names = (df['name'].iloc[df_indices]).tolist()
    return (names)
def counter(x,l,d_cal,basic):
    x = x.strip('][').split(',')
    x=list(set(x))
    xx=[]
    for i in x:
        if(len(i)>=1):
            if(i[1]=="\'"):
                i=i[2:-1]
            else:
                i=i[1:-1]
            xx.append(i)
            print(i,type(i))
            if(i not in basic):
                if(i not in l):
                    return(0,0)
    print("over")
    ct=0
    calorie=0
    for i in l:
        if(i in xx):
            calorie+=d_cal[i]
            ct+=1
    print(ct)
    return([ct//len(x),calorie])
def recipes_count(s,vnv,d_cal,basic,l):
    df=pd.read_csv(s)
    df = df['keyword']
    df_n=pd.read_csv(s)
    df_n = df_n['name']
    df_vnv=pd.read_csv(s)
    df_vnv = df_vnv['veg/nonveg']
    vnv_df=df_vnv.values.tolist()
    name_df=df_n.values.tolist()
    d={}
    lst=[]
    ctr=0
    ing_name_df=df.values.tolist()
    if(vnv=='all'):
        for i in ing_name_df:
            complex_list=counter(i,l,d_cal,basic)
            ct=complex_list[0]
            calorie=complex_list[1]

            if (ct not in lst):
                d[ct] = [1, [[name_df[ctr],calorie]]]
                lst.append(ct)
            else:
                d[ct][0] += 1
                d[ct][1].append([name_df[ctr],calorie])
            ctr += 1
    else:
        for i in ing_name_df:
            if(vnv_df[ctr]==vnv):
                ct,calorie=counter(i,l,d_cal,basic)
                if(ct not in lst):
                    d[ct]=[1,[[name_df[ctr],calorie]]]
                    lst.append(ct)
                else:
                    d[ct][0]+=1
                    d[ct][1].append([name_df[ctr],calorie])
            ctr+=1
    d_lst=[]
    for i in d:
        if(i!=0):
            d_lst.append([i,d[i]])
    d_lst.sort(key=lambda x:x[0])
    d_lst.reverse()
    return(d_lst)
@app.route('/',methods=['GET','POST'])
def hello_world():
    global detected
    global l
    global rl
    global d_lst
    global d_cal
    global sb
    global recom
    sb=[]
    detected = []
    l = []
    rl = []
    d_lst = {}
    d_cal = {}
    '''recom = []
    cur = con.cursor()
    postgreSQL_se_Query = "SELECT rec from users"
    cur.execute(postgreSQL_se_Query)
    rows = cur.fetchall()
    cur.close()
    for i in rows:
        recom.append(i)'''
    return render_template('base.html')
@app.route('/video/',methods=['POST'])
def video():
    return render_template('about.html')
@app.route('/logg/',methods=['POST'])
def log():
    global detected
    global l
    global rl
    global d_lst
    global d_cal
    global sb
    sb = []
    detected = []
    l = []
    rl = []
    d_lst = {}
    d_cal = {}
    return render_template('login.html')
@app.route('/signn/',methods=['POST'])
def sign():
    return render_template('signup.html')
@app.route('/sd/',methods=['POST'])
def sd():
    email=request.form.get("email")
    name= request.form.get("username")
    password1 = request.form.get("password1")
    password2= request.form.get("password2")
    pswd=['!','@','#','*','%','_','^','$','-']
    res=[]
    cur = con.cursor()
    postgreSQL_select_Query = "select * from users where email = %s"
    cur.execute(postgreSQL_select_Query, (email,))
    rows = cur.fetchall()
    cur.close()
    if (rows):
        return render_template('login.html', error=0)
    if (len(password1)<8):
        res.append(1)
    if(password1!=password2):
        res.append(2)
    for i in password1:
        if(i in pswd):
            cur = con.cursor()
            postgres_insert_query = """ INSERT INTO users VALUES (%s,%s,%s)"""
            record_to_insert=(name,email,password1)
            cur.execute(postgres_insert_query,record_to_insert)
            con.commit()
            count=cur.rowcount
            print(count, "Record inserted successfully into users table")
            cur.close()
            return render_template('home.html')
    res.append(3)
    return render_template('signup.html',error=res)
@app.route('/newhome/',methods=['POST'])
def nh():
    global detected
    global l
    global rl
    global d_lst
    global d_cal
    global sb
    sb = []
    detected = []
    l = []
    rl = []
    d_lst = {}
    d_cal = {}
    return render_template('home.html')
@app.route('/ld/',methods=['POST'])
def ld():
    global recom
    global email
    res=[]
    email=request.form.get("email")
    password=request.form.get("password")
    cur = con.cursor()
    postgreSQL_select_Query = "select * from users where email = %s"
    cur.execute(postgreSQL_select_Query, (email,))
    rows = cur.fetchall()
    cur.close()

    if(rows):
        cur = con.cursor()
        postgreSQL_select_Query = "select password from users where email = %s"
        cur.execute(postgreSQL_select_Query, (email,))
        rows = cur.fetchall()
        cur.close()
        if(rows[0][0]==password):
            recom=[]
            cur = con.cursor()
            postgreSQL_se_Query = "SELECT rec from users where email = %s"
            cur.execute(postgreSQL_se_Query,(email,))
            r = cur.fetchall()
            cur.close()
            for i in r:
                recom.append(i[0])
            return render_template('home.html')
        else:
            return render_template('login.html',error=1)
    else:
        res.append(5)
        return render_template('signup.html',error=res)

@app.route('/home/',methods=['POST'])
def home():
    return render_template('index.html')
@app.route('/result1/',methods=['POST'])
def res1():
    return render_template('detectyes.html',result=detected)

@app.route('/result2/', methods=['POST'])
def res2():
    return render_template('detectno.html',result=detected)

@app.route('/firstno/', methods=['POST'])
def firstno():
    global detected
    res=request.form.getlist('ing')
    for i in res:
        detected.remove(i)
    return render_template('additems.html',result=detected)

@app.route('/additems/', methods=['POST'])
def additems():
    global detected
    global l
    lst = request.form['add']
    ans_lst = lst.split(",")
    detected.extend(ans_lst)
    for i in detected:
        if(i[0]==' '):
            l.append(i[1:])
        else:
            l.append(i)
    print(l)
    return render_template('detectyes.html',result=detected)
@app.route('/addamt/', methods=['POST'])
def addamt():
    global d_cal
    global basicingredients
    for i in l:
        x=float(request.form[i])
        cal = float(api(i))
        d_cal[i] =(cal * x) / 100
        print(i, cal, (cal * x) / 100)
    basicingredients=list(set(basicingredients))
    basicingredients.pop(-1)
    print(basicingredients)
    return render_template('basicing.html',result=basicingredients)
@app.route('/catresult/',methods=['POST'])
def catresult():
    global d_lst
    global st
    global lit
    global category
    global rl
    rl=[]
    option = request.form['options']
    st = "recipes_dataset//"+ option + ".csv"
    category=option+".csv"
    res1=request.form.getlist('veg')
    res2=request.form.getlist('nonveg')
    if(res1==[]):
        vnv="nonveg"
    elif(res2==[]):
        vnv ="veg"
    else:
        vnv="all"
    d_lst = recipes_count(st, vnv, d_cal, basicingredients, l)
    mct = 20
    for i in d_lst:
        print(i)
        print("\n")
        prev = mct
        mct = mct - i[1][0]
        print(mct)
        if (mct <= 0):
            print("ingredient match count:", i[0], "no of recipes:", prev, i[1][1][:prev - 1])
            rl.extend(i[1][1][:prev - 1])
            break
        else:
            print("ingredient match count:", i[0], "no of recipes:", i[1][0], i[1][1])
            rl.extend(i[1][1])
    res = pd.read_csv(st)
    res = res[["name", "ingredients", "directions", "calories"]]
    results=[]
    iswithin=0
    isnot=0
    for i in rl:
        res_new = res[res['name'] == i[0]]
        r = res_new.values.tolist()
        if (r[0][3] <= i[1]):
            iswithin=1
            results.append([0,r[0][0],r[0][3],r[0][1],r[0][2]])
            print("WITHIN THE RANGE")
            print(r[0][0], "\n")
            print(r[0][3], "\n")
            print(r[0][1], "\n")
            print(r[0][2], "\n")
        else:
            isnot=1
            results.append([1, r[0][0], r[0][3], r[0][1], r[0][2]])
            print("NOT WITHIN THE RANGE BUT MATCHING THE INGREDIENTS")
            print(r[0][0], "\n")
            print(r[0][3], "\n")
            print(r[0][1], "\n")
            print(r[0][2], "\n")
    lit=[results,0,0]
    if(iswithin==0 and isnot!=0):
        lit[2]=1
    elif(iswithin!=0 and isnot==0):
        lit[1]=1
    elif(iswithin!=0 and isnot!=0):
        lit[1]=1
        lit[2]=1
    return render_template('result.html',result=lit)

@app.route('/done/',methods=['POST'])
def done():
    global lit
    for i in lit[0]:
        x=i[1].split(' ')
        i[1]='_'.join(x)
    return render_template('selectrecipe.html',result=lit)
@app.route('/basic/',methods=['POST'])
def basic():
    return render_template('basicyes.html',result=basicingredients)
@app.route('/recommend/',methods=['POST'])
def recommend():
    l=[]
    print(recom)
    for i in recom:
        if(i!=None):
            x=i.replace('_',' ')
            l.append(x)
    print(l)
    ans = []
    if(l.count(None)==len(l) or len(l)==0):
        pass
    else:
        df = pd.read_csv(st)
        tfidf = TfidfVectorizer(stop_words="english")
        df["directions"] = df["directions"].fillna("")
        # Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
        overview_matrix = tfidf.fit_transform(df["directions"])
        similarity_matrix = linear_kernel(overview_matrix, overview_matrix)
        mapping = pd.Series(df.index, index=df["name"])
        for i in l:
            if(i!=None):
                ans.extend(recommend_recipe(i,mapping,similarity_matrix,df))
        print(ans)
    return render_template('recommend.html',result=ans[:6])
@app.route('/recresult/',methods=['POST'])
def rec():
    global recom
    recom=[]
    print("hi")
    print(lit)
    res2=request.form.getlist("options")
    print(res2)
    recom.extend(res2)
    '''cur = con.cursor()
    print("email",email)
    postgreSQL_Query = "UPDATE users SET rec='kk';"
    cur.execute(postgreSQL_Query)
    cur.close()'''
    print(recom)
    return render_template('index.html')

@app.route('/basicno/',methods=['POST'])
def basicno():
    global l
    global sb
    l.extend(basicingredients)
    for i in basicingredients:
        if (i not in super_basic):
            d_cal[i] = 0
        else:
            sb.append(i)
            d_cal[i] = 0
    '''if (sb != []):
        return render_template('supbasic.html', result=sb)
    else:'''
    return render_template('buffer.html')

@app.route('/basic2/',methods=['POST'])
def basic2():
    global basicingredients
    global d_cal
    global l
    global sb
    res = request.form.getlist('ing')
    for i in res:
        basicingredients.remove(i)
    l.extend(basicingredients)
    for i in basicingredients:
        if (i not in super_basic):
            d_cal[i] = 0
        else:
            sb.append(i)
            d_cal[i] = 0
    '''if(sb!=[]):
        return render_template('supbasic.html',result=sb)
    else:'''
    return render_template('buffer.html')

@app.route('/supbasicres/',methods=['POST'])
def supbasicres():
    global d_cal
    for i in sb:
        x=float(request.form[i])
        cal = float(api(i))
        d_cal[i] =(cal * x) / 100
        print(i, cal, (cal * x) / 100)
    return render_template('buffer.html')
@app.route('/buff/',methods=['POST'])
def buff():
    global basicingredients
    lst = request.form['add']
    ans_lst = lst.split(",")
    basicingredients.extend(ans_lst)
    return render_template('category.html', result=datasets)
@app.route('/recipe',methods=['POST'])
def predict():
    global detected
    path='/Users/manasiswain/PycharmProjects/pythonProject/yolov5/runs/train/exp/test_images'
    if(os.path.isdir(path)):
        shutil.rmtree('/Users/manasiswain/PycharmProjects/pythonProject/yolov5/runs/train/exp/test_images')
        print("% s has been removed successfully" % dir)
    os.mkdir(path)
    files = request.files.getlist("imagefile")
    for file in files:
        filename = secure_filename(file.filename)
        try:
            file.save('/Users/manasiswain/PycharmProjects/pythonProject/yolov5/runs/train/exp/test_images/'+filename)
        except FileNotFoundError:
            return
    os.system('python write.py > output.txt')
    f = open("output.txt", "r")
    l = []
    for x in f:
        if (x[:5] == "image"):
            l.extend((x[115:-1]).split(','))
        if(x[:5] == "video"):
            l.extend((x[156:-1]).split(','))
    l = list(set(l))
    print(l)
    if(' ' in l):
        l.remove(' ')
    detected = []
    for i in l:
        ctr = 0
        while (1):
            if (i[ctr].isalpha() == True):
                break
            ctr += 1
        detected.append(lemmatizer.lemmatize(i[ctr:]))
    detected = list(set(detected))
    os.system('clear')
    print("The items detected in the images:")
    print(detected)
    return render_template('recipe1.html',result=detected)


if __name__=='__main__':
    app.run(port=3002,debug=True)