"""Main code for hash"""

# IMPORTS
from array import array

# data structures:
# videos			[ size ]
# endpoints			[ ( center_latency, number_connections, [ (cache_id, cache_latency) ] ) ]
# requests			[ ( video_id, endpoint_id, number_requests ) ] ]
# cache servers		[ cache_capacity ]

# to calculate min latency, check different cases
# for each case, find latencies until minimum case is reached
# to find latencies, check which video is requested by which endpoint
# find minimum latency of cache/cache storage
# ensure cache storage space is well utilised based on priority:
#     priority determined by number of requests of video
#         highest priority given to high request, small size videos

# vid1 = [50, 26, 5]
# req1 = [[(0, 100), (1, 200)], [(0, 50), (2, 500)],
#         [(0, 25), (1, 50), (2, 300)]]
#

#variables
cacheIndex = 0
endpoints = []
requests = []

#INPUT FROM FILE
f = open("me_at_the_zoo.in", "r", encoding="ascii")

#Get data centre line
details = [int(i) for i in f.readline().split()]

#Get videos line
videos = [int(i) for i in f.readline().split()]

#Allocate data centre variables
V = details[0]
E = details[1]
R = details[2]
C = details[3]
X = details[4]

#Obtain endpoints
for x in range(0,E):
    endpoint = []
    a = [int(i) for i in f.readline().split()]
    endpoint.append(a[0])
    b = a[1]
    endpoint.append(b)
    c = []
    for i in range(0,b):
        c.append([int(i) for i in f.readline().split()])
    endpoint.append(c)
    endpoints.append(endpoint)

#Obtain all requests
for i in range(0,R):
    requests.append([int(i) for i in f.readline().split()])

def rate_video(size, requests):
    # type of requests should be [ ( endpoint, requests) ]
    rating = [0 for _ in range(E)]
    for i in range(len(requests)):
        rating[requests[i][0]] = requests[i][1] / size
    if sum(rating) > 0:
        norm_rating = [n / sum(rating) for n in rating]
    else:
        norm_rating = rating
    return norm_rating

def distro_weights(videos, requests):
    ratings = [[] for _ in range(len(videos))]
    for i in range(len(videos)):
        # set ratings[i] to rating list based on video_id and request index
        rq_coll = []  # "request collation"
        for r in requests:
            if r[0] == i:
                rq_coll.append((r[1], r[2]))
        ratings[i] = rate_video(videos[i], rq_coll)
    # print(ratings)
    return ratings

def distribute_videos(videos, requests, endpoints):
    caches = [[] for _ in range(C)]
    i = 0
    for e in endpoints:
        if e[2]:  # can find closest cache
            closest_cache = e[2][0]
            for cache in e[2]:
                # find cache closest to e
                if cache[1] < closest_cache[1]:
                    # found cache closer
                    closest_cache = cache

            v_index = 0
            # print(i, closest_cache)
            for v in distro_weights(videos, requests):
                # if video is most beneficial to this endpoint
                if v[i] == max(v) and v[i] > 0:
                    caches[closest_cache[0]] += [v_index]
                v_index += 1
        else:  # no caches
            pass
        i += 1
    return caches

caches = distribute_videos(videos, requests, endpoints)

#FORMAT TO VALID
final = str(len(caches))+"\n"+""
for i in range(0,len(caches)):
    final = final+str(i)+" "+str(caches[i])+"\n"
final = final.replace(',','')
final = final.replace('(','')
final = final.replace(')','')
final = final.replace('[','')
final = final.replace(']','')
final = final.replace('\n\n','\n')

#OUTPUT TO FILE
s = open('solution.out', 'w')
s.write(final)
s.close()




