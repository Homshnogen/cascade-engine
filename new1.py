import et

et.start()
print(et.ehe)
et.ehe = "dsfbvnbvnjhghjfgsfafnbv"
def d1(f):
  print('making 1')
  def ret(*args):
    print('doing 1')
    f(*args)
    print('done 1')
  return ret
def d2(f):
  print('making 2')
  @d1
  def ret(*args):
    print('doing 2')
    f(*args)
    print('done 2')
  return ret

def rrr(x):
  if type(x) is type(rrr):
    x()
rrr = d2(rrr)
rrr(et.start)

def echo(x):
  def ret():
    print(x)
  return ret

list1 = list()

def test1(f):
  print("a test")
  list1.append(f)
  # a courtesy
  return f

@test1
def temp():
  print("it works")
@test1
def temp():
  print("it really works")

for i in list1:
  i()

print(type(temp))