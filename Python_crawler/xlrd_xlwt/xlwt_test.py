#coding:utf8
import xlwt
workbook = xlwt.Workbook()
Sheet1 = workbook.add_sheet('Sheet1',cell_overwrite_ok = True)
title = ['a','b','c','d']
stus = [['lili',20,'girl','class2'],['alice',18,'girl','class1']]

for i in range(len(title)):
    Sheet1.write(0,i,title[i])

for j in range(len(stus)):
    for t in range(len(title)):
        Sheet1.write(j+1,t,stus[j][t])

workbook.save('C:/Users/Acer/Desktop/workbook2.xls')
print('Done')