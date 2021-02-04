import csv
hasil = {'a':2,'b':1,'c':9}
print(hasil)
hasil = sorted(hasil.items(), key=lambda x: x[1],reverse=True)

print(hasil[1][0])

a = []
b= [1,2,3]
a.append(b)
print(a)