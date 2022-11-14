import os
import sys
import nltk
import pandas as pd
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import requests
import ast
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

if __name__ == '__main__':
    #os.system('pip install -r ./yolov5/requirements.txt')
    os.system('python write.py > output.txt')
    f = open("output.txt", "r")
    l = []
    for x in f:
        if(x[:5]=="image"):
            l.extend((x[115:-1]).split(','))
    l=list(set(l))
    l.remove(' ')
    detected=[]
    for i in l:
        ctr=0
        while(1):
            if(i[ctr].isalpha()==True):
                break
            ctr+=1
        detected.append(lemmatizer.lemmatize(i[ctr:]))
    detected=list(set(detected))
    os.system('clear')
    print("The items detected in the images:")
    print(detected)
    print("Are all items there Y/N:")
    ans = input()
    if (ans == "N"):
        print("Do you want to delete anything from the items detected Y/N:")
        ans1 = input()
        if (ans1 == "Y"):
            print("Enter items to delete comma separated")
            ans_del = input()
            ans_del_lst = ans_del.split(",")
            print(ans_del_lst)
            for i in ans_del_lst:
                detected.remove(i)
        print("Do you want to add anything  Y/N:")
        ans2 = input()
        if (ans2 == 'Y'):
            print("Enter items to add comma separated")
            ans_st = input()
            ans_lst = ans_st.split(",")
            detected.extend(ans_lst)
    l = detected
    d_cal={}
    for k in l:
        cal=float(api(k))
        print("Enter the amount of "+k+"in grams:")
        cal_ing=int(input())
        d_cal[k]=(cal*cal_ing)/100
        print(k,cal,(cal*cal_ing)/100)
    datasets = ['recipes_dataset//indian.csv','recipes_dataset//dessert.csv', 'recipes_dataset//diabetic.csv',
                'recipes_dataset//side_dish.csv','recipes_dataset//salad.csv', 'recipes_dataset//gluten_free.csv',
                'recipes_dataset//keto.csv', 'recipes_dataset//low_carb.csv', 'recipes_dataset//mocktail.csv',
                'recipes_dataset//smoothie.csv']
    print("Choose category:")
    for i in datasets:
        print(i[17:-4],end=" ")
    print('\n')
    x = input()
    st = "recipes_dataset//" + x + ".csv"
    print("Enter non-veg/veg/all:")
    vnv = input()
    basic=['salt','sugar','pepper','oil','water','clove','cumin','cardamom','cinnamon','turmeric','powder','masala','anise','corriander','basil','mustard','oregano']
    super_basic=['oil','sugar']
    print("This is a basic ingredients list which we assume you have:")
    print(basic)
    print("Do you want to edit this list and add(Y/N):")
    bn=input()
    if(bn=="Y"):
        print("Enter items to delete comma separated")
        ans_del = input()
        ans_del_lst = ans_del.split(",")
        for k in ans_del_lst:
            basic.remove(k)
    for i in basic:
        if(i not in super_basic):
            d_cal[i]=0
        else:
            cal = float(api(i))
            print("Enter the amount of " + i + "in grams:")
            cal_ing = int(input())
            d_cal[i] = (cal * cal_ing) / 100
    l.extend(basic)
    print(l)
    d_lst = recipes_count(st,vnv,d_cal,basic,l)
    #print(d_lst)
    #water,salt,sugar,flour,butter,egg,ghee
    #cumin,coriander,turmeric,pepper,mustard,ginger
    print("Enter how many recipes should be returned")
    mct = int(input())
    prev = 0
    rl = []
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
    res = res[["name","ingredients","directions","calories"]]
    for i in rl:
        res_new = res[res['name'] == i[0]]
        r = res_new.values.tolist()
        if(r[0][3]<=i[1]):
            print("WITHIN THE RANGE")
            print(r[0][0], "\n")
            print(r[0][3], "\n")
            print(r[0][1], "\n")
            print(r[0][2], "\n")
        else:
            print("NOT WITHIN THE RANGE BUT MATCHING THE INGREDIENTS")
            print(r[0][0], "\n")
            print(r[0][3], "\n")
            print(r[0][1], "\n")
            print(r[0][2], "\n")