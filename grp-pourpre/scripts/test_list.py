from math import sqrt

marker_log = []
marker_log.append((1, 0))
marker_log.append((2,1))
marker_log.append((5,8))
#marker_log.append((10,1))

def distance(xa, xb, ya, yb):
    return sqrt(  (xb - xa)**2 + (yb - ya)**2  )

# for j in range(len(marker_log)):
#     i = j
#     print('i avant boucle =' + str(i))
#     for range(i) in range(len(marker_log)-j):
#         print('i dans la boucle =' + str(i))

def compare_distances(marklog):
    min_dist = distance(marklog[0][0], marklog[1][0], marklog[0][1], marklog[1][1])
    for i in range(len(marklog)):
        for j in range(len(marklog)):
            if i != j :
                dist = distance(marklog[i][0], marklog[j][0], marklog[i][1], marklog[j][1])
                if (dist<min_dist) :
                    min_dist = dist                
    return min_dist

print(compare_distances(marker_log))




    # i = j 
    # for i in range(len(marker_log)- j):
    #     print('i =' + str(i))
    #     print(distance(marker_log[i][0], marker_log[i+1][0], marker_log[i][1], (marker_log[i+1][1] )))