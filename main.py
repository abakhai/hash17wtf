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

# variables
cacheIndex = 0
endpoints = []
requests = []
read_ratings_from_file = False

# INPUT FROM FILE
filename = "trending_today"
f = open(filename + ".in", "r", encoding="ascii")

rating_file = filename + ".rtg"
if read_ratings_from_file:
    r = open(rating_file, "r")
    rated_videos = eval(r.read())
    print(rated_videos)


# Get data centre line
details = [int(i) for i in f.readline().split()]

# Get videos line
videos = [int(i) for i in f.readline().split()]

# Allocate data centre variables
V = details[0]
E = details[1]
R = details[2]
C = details[3]
X = details[4]

# Obtain endpoints
for x in range(0, E):
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

# Obtain all requests
for i in range(0, R):
    requests.append([int(i) for i in f.readline().split()])


# return available space in a cache
def available_space(cache):
    space = X
    for v_id in cache:
        space -= videos[v_id]
    return space


# return list of caches sorted by lowest ping
def find_closest_caches(endpoint):
    e = endpoint
    if e[2]:  # can find closest cache
        closest_caches = sorted(e[2])
        return closest_caches
    else:
        return ()


# return closest cache id, factoring in space required to allocate next video
def find_closest_available_cache(caches, endpoint, size):
    for cache in find_closest_caches(endpoint):
        if available_space(caches[cache[0]]) > size:
            return cache[0]
        else:
            pass
    return ()


# rate video in terms of size:popularity ratio for each endpoint, normalised
def rate_video(size, requests):
    # type of requests should be [ ( endpoint, requests) ]
    rating = [0 for _ in range(V)]
    for i in range(len(requests)):
        rating[requests[i][0]] = requests[i][1] / size
    return rating


# rate the full list of videos
def rate_videos_bulk(videos, requests):
    ratings = [[] for _ in range(len(videos))]
    for i in range(len(videos)):
        if i % (V/5) == 0:
            print(i, '/', V)
        # set ratings[i] to rating list based on video_id and request index
        rq_coll = []  # "request collation"
        for r in requests:
            if r[0] == i:
                rq_coll.append((r[1], r[2]))
        ratings[i] = rate_video(videos[i], rq_coll)
    # print(ratings)
    return ratings


def distribute_videos(videos, endpoints):
    caches = [[] for _ in range(C)]
    i = 0
    for e in endpoints:
        v_index = 0
        print(i, '/', E)
        # print(i, closest_cache)
        for v in rated_videos:
            # if video is most beneficial to this endpoint
            if v[i] == max(v) and v[i] > 0:
                # best_cache will be closest available, considering sizes of ones which
                # are already hosting videos
                best_cache = find_closest_available_cache(caches, e, videos[v_index])
                # if best_cache exists
                if best_cache:
                    caches[best_cache] += [v_index]
            v_index += 1
        else:  # no caches
                pass
        
        i += 1
    return caches


def fill_space(videos, requests, endpoints):
    pass


#FORMAT TO VALID
#example caches array with 5 caches and the videos they store, some store just one video, some none and some more
# caches = ((1,0),(2,3,4),(5),(),(5,4,6,3))

if not read_ratings_from_file:
    r = open(rating_file, "w")
    rated_videos = rate_videos_bulk(videos, requests)
    r.write(str(rated_videos))
    r.close()

caches = distribute_videos(videos, endpoints)

final = str(len(caches))+"\n"+""
for i in range(0,len(caches)):
    final = final+str(i)+" "+str(caches[i])+"\n"
final = final.replace(',','')
final = final.replace('[','')
final = final.replace(']','')
final = final.replace('\n\n','\n')



# myE = 0
# print(endpoints[myE])
# print(find_closest_caches(endpoints[myE]))

##print(videos)
##
##print(X)
##
# distribute_videos(videos, requests, endpoints)

#OUTPUT TO FILE
s = open(filename + ".out", 'w')
s.write(final)
s.close()
