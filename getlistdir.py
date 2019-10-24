import os
list=os.listdir("C:\\eclipse-workspace\\tlink_v\\WebRoot\\WEB-INF\\lib")
str=""
for v in list:
    str+=";"+"C:\\eclipse-workspace\\tlink_v\\WebRoot\\WEB-INF\\lib\\"+v
print(str[1:])