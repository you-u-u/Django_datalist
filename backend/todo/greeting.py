print('おはよう')

def member(*args):
  print(args)

member("tom", "john")

def greet(*args):
  name =",".join(f"{name}さん" for name in args)
  print(f"good morning {name}")

greet("jhon", "k")

# def greet(name, age):
#     print(f"Hello, my name is {name} and I am {age} years old.")

# info = {"name": "Bob", "age": 30}
# greet(**info)

def introduction(**kwargs):
  #name = kwargs.get("name", "secret")
  age = kwargs.get("age", "secret")
  address =kwargs.get("address")


  print(kwargs)
  print(f"私は {kwargs['name']} です。{age}歳で、{address}に住んでいます。")
  #print(f"私は {kwargs['name']} です。{kwargs['age']}歳で、{kwargs['address']}に住んでいます。")


info = {"name": "john", "age": 18}
# name = str(input("名前を入力してください"))
# age = int(input("年齢は"))
# address =str(input("お住まいは"))
# personal_date = {"name":name, "age":age, "address":address}
# #print(personal_date)
           
introduction(**info)

# word = "abcd"
# a = word.strip("a")
# print(a)

# a=['sato', 'suzuki','abe']*2
# b=a+ ['tanaka', 'kato']
# print(b)

# del b[3]
# print(b)

# print(b.pop(2))
# print(b.pop())
# print(b)

# print(b.index(max(b)))
# print(len(b))

# a = ('sato', 'suzuki','abe')
# print(a)
# print(f"どーと{sorted(a)}")
# print(a)
# print(type(sorted(a)))
# print(sorted(a))

# print(type(tuple(a)))

# d = dict(apple=10, orange=20)
# print(d)
# print(type(d))

# d = dict([['apple',10], ['orange',20]])
# d["apple"] = 30
# d["banana"] = 50
# print(d)
# print(d.pop("orange"))
# print(d)

a = [0,1,1,2,8,5,3,2]
# s = set(a)
# print(s)

# s = {0,1,2}
# s.add(4)
# print(s)

# s1 = {0,1,2}
# s2 = {1,2,3}

# s3 = s1 | s2
# print(s3)

# s4 =s1.union(s2)
# print(s4)

# s1 = {0,1,2}
# s2 = {1,2,3}

# s3 =s1 - s2 
# print(s3)

# s4 = s1.difference(s2)
# print(s4)


# s1 = {0,1,2}
# s2 = {1,2,3}

# s3 = s1^s2
# print(s3)

# s4 = s1.symmetric_difference(s2)
# print(s4)

# l1 = [1,2,3,4,5]
# l2 = [1,2,3,4,5]
# l3 = l1

# print("1:",l1,id(l1))

# l1.append(6)
# print("2:",l1,id(l1))

# print("3:",id(l2))
# print("4:",id(l3))

# num= int(input("数字は"))

# print("偶数" if num % 2 == 0 else "奇数")
# if num % 3 ==0 & num % 2==0:
#   print("6")
# elif num%2==0:
#   print("2")
# elif num%3==0:
#   print("3の倍数")
# else:
#   pass


# for i in range(5):
#   print(range(5))
#   print(i)
# arr =range(5)
# sum =0
# for i in arr:
#   sum+= i
# print(sum)

# i=1
# while i<100:
#   i*=2
#   print(i)

x = "a-b-c"
a = x.split(sep="-")
print(a)

# a=2
# b=1
# try:
#   print("start")
#   print(a/b)
# except:
#   print("0で割れません")
# else:
#   print("OK")

# l1=[]
# for i in range(5):
#   l1.append(i)

# l2=[i for i in range(5)]

# print(l1)
# print(l2)

# d={i:i*2 for i in range(5)}
# print(d)

# def show(b, a=4):
#   return(a,b)
# a,b=show(5,7)
# print(a)
# print(b)

def show(a,b,*args):
  print(a)
  print(b)
  print(args)
  for i in args:
    print(i)

show(1,2,3,4,5)
