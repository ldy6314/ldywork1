import pandas as pd
import os
import sqlite3 as sq3

cwd = os.getcwd()
cwd = cwd.split('\\')
parent = '/'.join(cwd[:-1])
bookdir = parent+'/score'
lst = os.listdir(bookdir)


conn = sq3.connect('score.sqlite3')
cur = conn.cursor()

sql = 'create table score(name text primary key, cls text, chn float, math float, eng float, sci float)'
try:
    cur.execute(sql)
except Exception as e:
    print(e)

class_list = []
for i in lst:
    print(i)
    filename = bookdir + '/' + i
    df = pd.read_excel(filename)
    info = list(df.columns.values)
    class_name = info[1] + str(info[3])
    class_list.append(class_name)
    class_list.sort()
    for info in df.values[1:]:
        print(info)
        sql = "insert into score values('{}', '{}', {}, {}, {}, {})".format(info[0], class_name, info[1], info[2],
                                                                            info[3], info[4])
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            pass

    print(100*'-')
# 获取每个班级的数据
stu_tot = {}
sql = 'select cls, count(*) from score group by cls'
cur.execute(sql)
ls = cur.fetchall()
for i in ls:
    stu_tot[i[0]] = i[1]


tot_info = {}
sql = 'select cls,avg(chn), avg(math), avg(eng), avg(sci), avg(chn+math+eng+sci) from score group by cls'
cur.execute(sql)
lst = cur.fetchall()
for sub in [('chn', 100), ('math', 100), ('eng', 100), ('sci', 50)]:
    print(sub[0])


with open('avg.csv', 'w', encoding='gbk') as f:
    f.write('班级,语文,数学,英语,科学,总分,及格率,优秀率\n')
    for i in lst:
        i = list(i)
        for j in range(1, 6):
            i[j] = '{:.2f}'.format(i[j])
        print(i)
        f.write(','.join(i)+'\n')

info = {}
for sub in [('chn', 100), ('math', 100), ('eng', 100), ('sci', 50)]:
    info[sub[0]] = {}
    sub_dict = info[sub[0]]
    for rg in [(100, 101), (95, 100), (90, 95), (85, 90), (80, 85), (75, 80), (70, 75), (65, 70), (60, 65), (0, 60),
               (90, 101)]:
        l_bound = rg[0]/100*sub[1]
        u_bound = rg[1]/100*sub[1]
        sub_dict[(l_bound, u_bound)] = {}
        dic = sub_dict[(l_bound, u_bound)]
        sql = 'select cls,count(*) from score where {}>={} and {}<{}  group by cls'.format(sub[0], l_bound,
                                                                                           sub[0], u_bound)
        cur.execute(sql)
        lst = cur.fetchall()
        for i in lst:
            dic[i[0]] = i[1]

print(stu_tot.items())

for sub in [('chn', 100), ('math', 100), ('eng', 100), ('sci', 50)]:
    print(sub)
    with open(sub[0]+'.csv', 'w', encoding='gbk') as f:
        to_write = []
        f.write("分数范围,"+','.join(class_list)+'\n')
        sub_info = info[sub[0]]
        for rg in [(100, 101), (95, 100), (90, 95), (85, 90), (80, 85), (75, 80), (70, 75), (65, 70), (60, 65), (0, 60),
                   (90, 101)]:
            jg = 0
            yx = 0
            if rg == (0, 60):
                jg = 1
            if rg == (90, 101):
                yx = 1
            rg = list(rg)
            rg[0] = rg[0]*sub[1]/100
            rg[1] = rg[1]*sub[1]/100
            rg = tuple(rg)
            print(str(rg).replace(',', '-'). replace('(', '['), end=',',file=f)
            rg_info = sub_info[rg]
            for cls in class_list:
                if yx:
                    yxl = rg_info.get(cls, 0)/stu_tot[cls]*100
                    print("{:.2f}%".format(yxl), end=',', file=f)
                elif jg:
                    jgl = (stu_tot[cls]-rg_info.get(cls, 0))/stu_tot[cls]*100
                    print("{:.2f}%".format(jgl), end=',', file=f)
                else:
                    print(rg_info.get(cls, 0), end=',', file=f)
            print(file=f)

