import json

data = {}
new_data = []

with open("input.json", "r") as read_file:
    data = json.load(read_file)

for i in data:
  if type(i) == type([]):
    new_list = []
    for j in i:
      if j % 2:
        new_list += [j]
    new_data += [new_list]
    
  elif type(i) == type(dict()):
    buf = dict()
    for j in i:
      if j.lower().__contains__("key"):
        buf.update({j.upper(): i[j]})
    new_data += [buf]
    
  elif type(i) == type(""):
    new_data += [i[0:len(i)//2]]
  else:
    new_data += [i]

with open("output1.json", "w") as outfile:
  json.dump(new_data, outfile, indent=True)
  
