import  pandas

upload = pandas.read_csv("linked.csv", encoding='utf-8')
def printja(data):
    l = []
    if data == "None" or data == None:
        l.append("None")
    else:
        for i in data:
            l.append(upload['url'][i])

    return l


#a = printja({0,1,2})
#print(a)