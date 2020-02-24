import os
import json

def pyThag(x1, y1, x2, y2):
    a = (float(x2)-float(x1)) #a = difference in x
    b = (float(y2)-float(y1)) #b = difference in y
    return (a**2+b**2)**(1/2) #c = sqrt(a^2 + b^2)

def getIslands(file = 'all_islands.json'):
    with open(file, 'r') as f:
        islands = json.load(f)
    return islands

""" ABSOLUTE FASTEST VOYAGE ALGORITHM """


def fastestVoyage(islandCoords, visit):
    
    #define start island and distance to start island
    distances = [0]       #time structure:   [time1, time2]
    voyage = [[visit[0]]] #voyage structure: [[island 1, island 2, island 3],
    #                                         [island 1, island 3, island 2]]

    #base case saying if theres only 1 left in visits we are already here return the distance
    if len(visit) <= 1:
        return distances, voyage

    #loop through all islands besides start island to find all possible routes
    #from start island.
    #each recursive call will set the start island to visit[i] in the previous function call

    #each recursive call would create a new layer and each loop would create a new branch:

    #           island_1                         _____________island_1____________
    #          /        \                       /                |                \
    #     island_2     island_3           island_2            island_3           island_4
    #       /              \              /     |           /        \            |      \
    #   island_3        island_2     island_3  island_4   island_2  island_4   island_2  island_3
    #                                   |        |          |           |        |          |
    #                                island_4  island_3   island_4  island_2   island_3  island_2

    for i in range(1, len(visit[1:])+1):
        
        #distance between start island (visit[0]) and current loop island (visit[i])
        distance = pyThag(float(islandCoords[visit[0]][0]), float(islandCoords[visit[0]][1]),
                          float(islandCoords[visit[i]][0]), float(islandCoords[visit[i]][1]))
        
        otherVisit = [visit[i]]+visit[1:i]+visit[i+1:]
        subVoyage = fastestVoyage(islandCoords, otherVisit)

        #each loop check there is enough room in the voyage. used on the smaller branches
        if len(voyage) < i:
            voyage.append([visit[0]])

        if len(distances) < i:
            distances.append(0)

        #loop through all possible routes from the previous recursive call
        for j in range(len(subVoyage[1])):

            #if the last item in voyage is the length of a completed route
                #try concatonate the previous voyage with the voyage from the jth last recursive call.
                #   and add to the total value
                #if there are more possible voyages from the recursive call than in the voyage list, append this to as a new route in the voyage and a new distance for this new route
            #else an error is raised and and append as new route in the voyage and a new distance for this new route

            try:
                if len(voyage[-1])==len(visit):
                    raise Exception
                voyage[len(voyage)-1+j] = voyage[len(voyage)-1+j]+subVoyage[1][j]
                distances[len(distances)-1+j] += distance+subVoyage[0][j]
            except:
                voyage.append([visit[0]]+subVoyage[1][j])
                distances.append(distance+subVoyage[0][j])
    
    """ DEPENDS ON DATA STRUCTURE """
    return distances, voyage



""" ######## MAIN CODE ######## """

islands = getIslands() #dictionary of all islands and coords {name: [x,y],
                       #                                      name: [x,y]}

sample = [i for i in islands.keys()][:6] #list of the island names to visit [name, name]
coords = {i:islands[i] for i in sample}  #dictionary of the coordinates for these islands
print('list of island names\n',sample)
print('\ndictionary of island names:coordinates\n',coords,'\n')


#####################################

voyage = fastestVoyage(coords, sample) #call the function
print(voyage)

#voyage contains a tuple (list of distances, list of journeys)
#route = the journey that corresponds with the lowest distance value
route = voyage[1][voyage[0].index(min(voyage[0]))]
print(route)
