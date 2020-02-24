import json

with open('outposts.json','r') as f:
    islands = json.load(f)

print(islands)

new_islands = {}

for i in islands:
    new_islands[i.title()] = islands[i]

print('\n\n',new_islands)

with open('outposts.json','w') as f:
    json.dump(new_islands, f)
