print (C)
for cache in caches:
    #print cacheIndex
    print (cacheIndex, end=" ")
    cacheIndex += 1
    
    #if no video is stored in this cache
    if not cache:
        print ()
    #if just one video is stored in this cache
    elif isinstance(cache, int):
        print (cache)
    #if more than one video is stored in this cache
    else:
        for video in cache:
           print (video, end=" ")
        print ()