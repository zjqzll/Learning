# encoding: utf8
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def load(path):
    txtlists = os.listdir(path)
    readresult = []
    for txt in txtlists:
        f = open(path + '/' + txt)
        lines = f.readlines()
        pattern = re.compile(r'[a-z]+([0-9]+).txt')
        year = re.search(pattern, txt).group(1)
        for line in lines:
            linelist = line.split(',')
            tmp = linelist[2].replace('\n', '')
            linelist[2] = int(tmp)
            linelist.append(int(year))
            readresult.append(linelist)

    df = pd.DataFrame(readresult, columns=['name', 'sex', 'births', 'year'])
    return df


def load2(path):
    years = range(1880, 2019)
    result = []
    for year in years:
        frame = pd.read_csv(path + '/' + f'yob{year}.txt',
                            names=['name', 'sex', 'births'])
        frame['year'] = year
        result.append(frame)
    df = pd.concat(result, ignore_index=True)
    return df


def add_prop(data):
    data['prop'] = data.births / data.births.sum()
    return data


def addprop(rawdata):
    rawdata = rawdata.groupby(['year', 'sex']).apply(add_prop)
    return rawdata


def sex_births(rawdata):
    sex_birth_num = pd.pivot_table(rawdata, index='year', columns='sex',
                                   values='births', aggfunc='sum')
    sex_birth_num.plot(title='Total births by sex and year',
                       xticks=range(1880, 2025, 10))
    plt.xlabel('Year')
    plt.ylabel('Births')
    plt.savefig('0 Total births by sex and year.png')
    plt.show()
    return sex_birth_num


def wordcloudfunc(data, pname):
    wordcloud = WordCloud(background_color='white', width=800, height=660,
                          margin=2, collocations=False, relative_scaling=0,
                          normalize_plurals=False).generate(
        data)
    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud.to_file(pname)


def get_top1000(rawdata):
    top1000_list = []
    for year, group in rawdata.groupby(['year', 'sex']):
        top1000_list.append(
            group.sort_values(by='births', ascending=False)[:1000])

    top1000_df = pd.concat(top1000_list, ignore_index=True)
    return top1000_df


def count_number(data, q=0.5):
    data = data.sort_values(by='prop', ascending=False)
    position = data.prop.cumsum().values.searchsorted(q) + 1
    return position


def name_diversity(top1000data):
    table = pd.pivot_table(top1000data, index='year', columns='sex',
                           aggfunc='sum', values='prop')  # Top1000 中 sum(prop)
    table.plot(title='Sum of top1000data.prop by year and sex',
               yticks=np.linspace(0.5, 1.2, 10), xticks=range(1880, 2025, 10))
    plt.xlabel('Year')
    plt.ylabel('Prop')
    plt.savefig('1 Sum of top1000data.prop by year and sex.png')
    number_name_q = top1000data.groupby(['year', 'sex']).apply(
        count_number)  # Top1000 中 sum(prop) = 50% 的 num(name)
    numbername = number_name_q.unstack('sex')
    numbername.plot(title='Number of popular names in top 50%',
                    xticks=range(1880, 2025, 10))
    plt.xlabel('Year')
    plt.ylabel('Number')
    plt.savefig('2 Number of popular names in top 50%.png')
    plt.show()

    return table, number_name_q


def name_births_prop(rawdata):
    name_births = pd.pivot_table(rawdata, index='name', columns=['sex', 'year'],
                                 values='births', aggfunc='sum')
    yearindex = [1880, 1915, 1950, 1985, 2018]
    name_births_year = name_births.reindex(columns=yearindex, level='year')
    name_births_prop = name_births_year / name_births_year.sum()
    # print(name_births_prop)
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    i = 0
    for s in ['F', 'M']:
        j = 0
        for y in yearindex:
            boys_sort = name_births_prop[s][y].dropna(axis=0,
                                                      how='all').sort_values(
                ascending=False)[:5]
            boys_sort_index = list(boys_sort.index)
            boys_sort_frame = boys_sort.to_frame()  # .reset_index(drop=True)
            axes[i, j].plot(boys_sort_frame, marker='o')
            plt.suptitle('Top5(name) of 1880, 1915, 1950, 1985, 2018')
            j += 1
        i += 1

    plt.savefig('3 Top5 of name by sex and year.png')
    plt.show()


def get_first_letters(rawdata):
    rawdata['first_letter'] = rawdata.name.map(lambda x: x[0])

    table = pd.pivot_table(rawdata, index='first_letter',
                           columns=['sex', 'year'], values='births',
                           aggfunc='sum')
    letter_prop_table = table / table.sum()
    letter_prop_year = letter_prop_table.reindex(
        columns=[1880, 1900, 1920, 1940, 1960, 1980, 2000, 2018], level='year')

    fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(20, 10))
    letter_prop_year['F'].plot(kind='bar', rot=0, ax=axes[0], title='Female')

    letter_prop_year['M'].plot(kind='bar', rot=0, ax=axes[1], title='Male')
    plt.xlabel('First letter of name')
    plt.ylabel('Prop')
    plt.suptitle('First letter of name by sex and year')
    plt.savefig('4 First letter of name by sex and year.png')
    plt.show()


def nochangename(rawdata):
    name_pivot = pd.pivot_table(rawdata, index='name', columns=['sex', 'year'],
                                values='births', aggfunc='sum')
    girls = name_pivot['F'].dropna(axis=0, how='any')
    boys = name_pivot['M'].dropna(axis=0, how='any')

    girls_sort = girls.sum(axis=1).sort_values(ascending=False)
    girls_sort_txt = ' '.join(list(girls_sort.index))

    print(f'girls: {girls_sort_txt}')
    # print(len(set(girls_sort.index)))
    boys_sort = boys.sum(axis=1).sort_values(ascending=False)
    boys_sort_txt = ' '.join(list(boys_sort.index))
    # print(type(boys_sort_txt))
    print(f'boys: {boys_sort_txt}')
    return girls_sort_txt, boys_sort_txt


def file(data):
    f1 = open('result.txt', 'w')
    f1.write('\n'.join(data))
    f1.close()


if __name__ == '__main__':
    path = r'F:\0_研究生\3学习\Data analysis\0 资料\pydata-book-2nd-edition\datasets\babynames'
    raw_data = load(path)
    # print(raw_data.info())
    # print()
    # print(raw_data.count())
    prop_data = addprop(raw_data)
    sexbirthnum = sex_births(raw_data)
    Top1000_data = get_top1000(prop_data)
    sumprop, numname = name_diversity(Top1000_data)
    name_births_prop(raw_data)
    get_first_letters(raw_data)
    girls, boys = nochangename(raw_data)
    wordcloudfunc(boys, pname='Boys.png')
    wordcloudfunc(girls, pname='Girls.png')
    # data = open(r'F:\0_研究生\3学习\Data analysis\1 实战\0 babyname\Analysis/txt.txt', 'r').read()
    # wordcloudfunc(data, pname='txt.png')
