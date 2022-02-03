from random import randint, randrange

def random_int_list(n, bound):
    res = []
    for _ in range(n):
        res.append(randrange(0,bound))
    return res

def random_int_matrix(n, bound):
    res = []
    for _ in range(n):
        res.append(random_int_list(n,bound))
    return res

def random_int_matrix(n, bound, null_diag=True):
    res = []
    for i in range(n):
        res.append(random_int_list(n,bound))
        if null_diag:
            res[i][i] = 0
    return res

def random_symetric_int_matrix(n, bound, null_diag = True):
    res = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(i + 1, n):
            res[i][j] = res[j][i]
    return res

def random_oriented_matrix(n ,bound, null_diag=True):
    res = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(i + 1,n):
            rd = randint(0,1)
            if rd==1 :
                res[j][i]= 0
            else:
                res[i][j]= 0 
    return res

def random_triangular_int_matrix(n ,bound, null_diag = True):
    res = random_int_matrix(n,bound,null_diag)
    for i in range(n):
        for j in range(i + 1, n):
            res[i][j] = 0
    return res 



#print(random_triangular_int_matrix(4,10,False))