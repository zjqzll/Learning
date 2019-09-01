# coding:utf8
# import xlrd
# workbook = xlrd.open_workbook(u'C:/Users/Acer/Desktop/workbook1.xlsx')
# print(workbook.sheet_names())
# workbook1 = workbook.sheets()[0]
# workbook2 = workbook.sheet_by_index(0)
# workbook3 = workbook.sheet_by_name('Sheet1')
#
# num_rows = workbook1.nrows
# num_cols = workbook1.ncols
#
# first_row = workbook1.row_values(0)
# first_col = workbook1.col_values(0)
#
# print(first_row)
#
# for cur_row in range(num_rows):
#     for cur_col in range(num_cols):
#         val = workbook1.cell_value(cur_row,cur_col)
#         print('row%s col%s value is %s'%(cur_row,cur_col,val))
b = 0
for i in range(1,11):
    a = 8-i
    if a == 0:
        break
    else:
        b +=1
        print('i={}'.format(i))
        print('a={}'.format(a))
