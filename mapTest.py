def add_one(num):
  new_num = num + 1
  print(new_num)
  return new_num
my_list = [1, 3, 6, 7, 8, 10]
f = map(add_one, my_list)
r = next(f)
r = next(f)
print(r)
