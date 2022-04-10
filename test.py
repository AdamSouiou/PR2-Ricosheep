lst = [(4,6),(3,8),(2,9)]

def tri(duo):
    x,y = duo
    return x

lst.sort(key=tri)
print(lst)