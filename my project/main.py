import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches

grad = 'Graduation'
ru = 'Title_ru'
en = 'Title_en'
st = 'Student'
year = 'Years'
lvl = 'Level'
fac = 'Faculty'
sp = 'Speciality'
op = 'OP'
op_t = 'OP_title'
adv = 'Advisor'
pos = 'Position'
deg = 'Degree'
dep = 'Department'
dep_fac = 'DepFaculty'

pu = 'Процессы управления'
mm = 'Математика и механика'
mkn = 'Математика и компьютерные науки'

fac_names = [pu,mm,mkn]

table = pd.read_excel('VKR_eng.xlsx')

def StatByYears():
    sns.histplot(data=table, x=grad, hue=fac, bins=20, palette='dark')
    plt.show()

def StatByFac():
    fig, axes = plt.subplots(1, 3)
    axes[0].set_title('ПМПУ')
    axes[1].set_title('МатМех')
    axes[2].set_title('МКН')
    sns.histplot(ax=axes[0], data=table[table[fac] == pu], x=lvl, hue=fac)
    sns.histplot(ax=axes[1], data=table[table[fac] == mm], x=lvl, hue=fac)
    sns.histplot(ax=axes[2], data=table[table[fac] == mkn], x=lvl, hue=fac)
    plt.show()

def StatBySurname():
    st_names = table[st].sort_values()
    letters_count = {}
    for name in st_names:
        first_letter = name[0].upper()
        if first_letter in letters_count:
            letters_count[first_letter] += 1
        else:
            letters_count[first_letter] = 1
    plt.bar(letters_count.keys(), letters_count.values())
    plt.xlabel('первая буква фамилии')
    plt.ylabel('количество ВКР')
    plt.show()

def BadStatByMyName():
    sofya_counts = table[st].str.count('Софья').sum()
    sofia_counts = table[st].str.count('София').sum()
    other_counts = len(table) - sofya_counts - sofia_counts
    plt.bar(['Софья','София','Остальные'], [sofya_counts, sofia_counts, other_counts])
    plt.show()

def NormStatByMyName():
    sofya_counts = table[st].str.count('Софья').sum()
    sofia_counts = table[st].str.count('София').sum()
    plt.bar(['Софья','София'], [sofya_counts, sofia_counts])
    plt.show()

def MLbyYears():
    table['with_ml'] = table[en].str.contains('machine learning')
    gr = table.groupby(grad)['with_ml'].sum()
    plt.title('Machine Learning')
    plt.bar(gr.index, gr.values)
    plt.show()

def ThemesByYears():
    table['ml'] = table[en].str.contains('machine learning')
    table['bd'] = table[en].str.contains('BigData')
    table['m'] = table[en].str.contains('modeling')
    table['3d'] = table[en].str.contains('3D')
    gr = table.groupby(grad)[['ml','bd','m','3d']].sum()
    plt.plot(gr.index, gr['ml'], label='Machine Learning')
    plt.plot(gr.index, gr['bd'], label='BigData')
    plt.plot(gr.index, gr['m'], label='Modeling')
    plt.plot(gr.index, gr['3d'], label='3D')
    plt.xlabel('годы')
    plt.ylabel('количество ВКР')
    plt.legend()
    plt.show()

def KIS():
    table['psi'] = table[adv]=='Перегудин Сергей Иванович'
    table['mav'] = table[adv] == 'Матросов Александр Васильевич'
    table['eas'] = table[adv] == 'Еремин Алексей Сергеевич'
    table['oiv'] = table[adv] == 'Олемской Игорь Владимирович'
    table['kan'] = table[adv] == 'Квитко Александр Николаевич'
    gr = table.groupby(grad)[['psi','mav','eas','oiv','kan']].sum()
    plt.plot(gr.index, gr['psi'], label='Перегудин С.И.')
    plt.plot(gr.index, gr['mav'], label='Матросов А.В.')
    plt.plot(gr.index, gr['eas'], label='Еремин А.С.')
    plt.plot(gr.index, gr['oiv'], label='Олемской И.В.')
    plt.plot(gr.index, gr['kan'], label='Квитко А.Н.')
    plt.title('кафедра информационных систем')
    plt.legend()
    plt.show()

def KIS2():
    sns.histplot(data=table[table[dep]=='Кафедра информационных систем'], x=grad, hue=lvl, bins=20, palette='dark')
    plt.show()

def NameAndThemes():
    fig, axes = plt.subplots(1, 4)
    table['first_letter'] = table[st].str[0]
    gr = table.groupby('first_letter')
    for i, (name, group) in enumerate(gr):
        if en in group.columns:
            group['ml'] = group[en].str.contains('machine learning', case=False).sum()
            group['bd'] = group[en].str.contains('BigData', case=False).sum()
            group['m'] = group[en].str.contains('modeling', case=False).sum()
            group['3d'] = group[en].str.contains('3D', case=False).sum()

            axes[0].bar(name, group['ml'])
            axes[1].bar(name, group['bd'])
            axes[2].bar(name, group['m'])
            axes[3].bar(name, group['3d'])
    axes[0].set_title('Machine Learning')
    axes[1].set_title('BigData')
    axes[2].set_title('Modeling')
    axes[3].set_title('3D')
    plt.show()

def NameAndDep():
    fig, axes = plt.subplots(1, 4)
    table['first_letter'] = table[st].str[0]
    gr = table.groupby('first_letter')
    for i, (name, group) in enumerate(gr):
        if dep in group.columns:
            group['cm'] = group[dep].str.contains('Кафедра компьютерного моделирования и многопроцессорных систем', case=False).sum()
            group['ia'] = group[dep].str.contains('Кафедра информационно-аналитических систем', case=False).sum()
            group['sp'] = group[dep].str.contains('Кафедра системного программирования', case=False).sum()
            group['tp'] = group[dep].str.contains('Кафедра технологии программирования', case=False).sum()

            axes[0].bar(name, group['cm'])
            axes[1].bar(name, group['ia'])
            axes[2].bar(name, group['sp'])
            axes[3].bar(name, group['tp'])
    axes[0].set_title('computer modeling')
    axes[1].set_title('information and analytical systems')
    axes[2].set_title('system programming')
    axes[3].set_title('technology of programming')
    plt.show()

#StatByYears()
#StatByFac()
#StatBySurname()
#BadStatByMyName()
#NormStatByMyName()
#MLbyYears()
#ThemesByYears()
#KIS()
#KIS2()
#NameAndThemes()
#NameAndDep()

