#-*- coding:utf-8 -*-
import numpy
import random
import csv
#文件名file_name
#验证集百分比percentage 10 意味着10%

#----------------读取数据----------------
def Create_training_data_and_test_data(file_name,percentage):
    reader=csv.reader(open(file_name, 'r'))
    sum_of_file=0
    train = []
    test = []
    for item in reader:

        sum_of_file=sum_of_file+1
        uId = int(item[0])
        mId = int(item[1])
        ratingstars = float(item[2])
        time = float(item[3])


        x=random.randint(1, 100)
        if ( x> percentage):
            train.append([uId, mId, ratingstars,time])
        else:
            test.append([uId, mId, ratingstars,time])

    #print("读取数据完毕，共有%d条" % sum_of_file)
    #print("训练集%条，测试集%d条" % (len(train),len(test)))

    trainname = file_name.replace('.csv',"_train.csv")
    testname = file_name.replace('.csv',"_test.csv")
    numpy.savetxt(trainname, train, delimiter=',')
    numpy.savetxt(testname, test, delimiter=',')
    return trainname,testname

Create_training_data_and_test_data('data/ratings.csv',10)