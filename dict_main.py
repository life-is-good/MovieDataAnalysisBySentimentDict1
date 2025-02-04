# -*- coding: utf-8 -*-
import xlrd						#模块xlrd：读取excel
import xlwt						#模块xlwt：写入excel
import comment
from comment import Comment
import ConfigParser				#模块ConfigParser：读写配置文件

conf = ConfigParser.ConfigParser()		#对象conf：生成的config对象
conf.read('settings.cfg')				#读取配置文件settings.cfg内容赋给conf

#初始化读取表格的页，列#
sheet_num = conf.getint('excel_settings','sheet_num')		#读取conf中excel_settings段落中sheet_num变量值（整型）赋给sheet_num
column_comment_num = conf.getint('excel_settings', 'column_comment_num')	#读取conf中excel_settings段落中column_comment_num变量值（整型）赋给column_comment_num
column_date_num = conf.getint('excel_settings', 'column_date_num')   #读取conf中excel_settings段落中column_date_num变量值（整型）赋给column_comment_num  
begin_row = conf.getint('comment_settings', 'begin_row')	#读取conf中comment_settings段落中begin_row变量值（整型）赋给begin_row
end_row = conf.getint('comment_settings', 'end_row')		#读取conf中comment_settings段落中end_row变量值（整型）赋给end_row
input_file = (conf.get('file_settings', 'input_file')).decode('GBK')	#读取conf中file_settings段落中input_file变量值（文本字节流）用GBK编码并赋给input_file
output_file = (conf.get('file_settings', 'output_file')).decode('GBK')	#读取conf中file_settings段落中output_file变量值（文本字节流）用GBK编码并赋给output_file


#分类#
classification = comment.classification

print 'start'

#读excel#
if 1:
    #打开表格#
    table_data = xlrd.open_workbook( input_file)
    #获取一个工作表#
    table = table_data.sheet_by_index( sheet_num )
    #获取整列数据#
    col_comment = table.col_values(column_comment_num )
    col_date = table.col_values(column_date_num )
    nrows = table.nrows
    #写入表格#
    table_w = xlwt.Workbook()
    #工作表名称#
    sheet1 = table_w.add_sheet('result')				#写入表表名为result，赋给变量sheet1
    #写sheet的第一行
    countTotal=[]
    countGood=[]
    for j in range(len(classification)):
        sheet1.write(0,j+2,classification[j][0])		#第一行第三列开始：录入classification中每个元素列表的第一个元素
        countTotal.append(0)
        countGood.append(0)
    sheet1.write(0,0, u'点评内容') 						#第一行第一列：点评内容
    sheet1.write(0,1, u'点评时间') 						#第一行第二列：点评内容

    row = 0					#有效点评内容行数
    k = 0					#点评内容行数
    for i in range(nrows) :		#遍历点评这一列，每行点评内容放到col_comment[i]
        if col_comment[i] == u'':			#若为空，则k+=1,continue
            k += 1
            continue
        if col_comment[i] == u'点评内容':	#若为点评内容，则都自加，continue
            row += 1
            k += 1
            continue
        if  row < begin_row:		#若还不到设定起始行，都自加，continue？为啥不到起始行要都自加？
            row += 1
            k += 1
            continue
        if row > end_row:			#若有效点评行超过设定截止行，终止
            break
        #遇到空格跳过#
        col_comment[i] = col_comment[i].replace('<br/>','')
        col_comment[i] = col_comment[i].replace('&nbsp;','')
        col_comment[i] = col_comment[i].replace('\n','')

        comment = Comment(col_comment[i])
        comment.calScore()
        print '\nComment',row,':'
        print col_comment[i].strip('\n')
        comment.printScore()
        j = 2
        flag = 0
        for score in comment.average_score:
            if score != -1:
                flag = 1
                sheet1.write(row,j,score)
                countTotal[j-2]+=1
                if score>=7:
                    countGood[j-2]+=1
            j += 1
        if flag == 0:
            sheet1.write(row, j-1, col_date[i]*2)#没有关键字的时候打分按照原先的星级评分来打分，但是要转换成10分制的打分，原先的星级评分满分是五分，所以暂时将星级分数加倍
        sheet1.write(row,0,col_comment[i])
        sheet1.write(row,1,col_date[k])
        #sheet1.write(row,j,col_time[k])
        row += 1
        k += 1
        
    
    for j in range(len(classification)):
        sheet1.write(row,j+2,countTotal[j])		#第一行第三列开始：录入classification中每个元素列表的第一个元素
        sheet1.write(row+1,j+2,countGood[j])
    sheet1.write(row,0, u'有效评论数') 						#第一行第一列：点评内容
    sheet1.write(row+1,0, u'好评数')
    
    table_w.save(output_file)

# else:
#     fileHandler = open('test.txt') #以读写方式处理文件IO
#     fileHandler.seek(0)
#     i = 0
#     for col_comment[i] in fileHandler.readlines():
#         col_comment[i] = col_comment[i].decode('utf-8')
#         if col_comment[i] == u'\n':
#             continue
#         i = i + 1
#         col_comment[i] = col_comment[i].replace('<br/>','')
#         col_comment[i] = col_comment[i].replace('&nbsp;','')
#         col_comment[i] = col_comment[i].replace('\n','')
#         comment = Comment(col_comment[i])
#         comment.calScore()
#         print '\nComment',i,':'
#         print col_comment[i].strip('\n')
#         comment.printScore()
    
print 'finished'
    


