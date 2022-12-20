import sys

def changeNegation(s):
    if type(s) == str:
        return ['not', s]
    elif s[0] == 'not':
        return s[1]
    elif s[0] == 'and':
        temp = ['or']
        for element in s[1:]:
            temp.append(changeNegation(element))
        return temp
    elif s[0] == 'or':
        temp = ['and']
        for element in s[1:]:
            temp.append(changeNegation(element))
        return temp
    else:
        s_temp = str(s)
        return ('not', s_temp[1:len(s_temp) - 1])


def disCombine(op, clause):
    result = []
    if type(clause) == str:
        return [clause]
    elif len(clause) <= 2:
        return [clause]
    elif op == clause[0]:
        return clause[1:]
    else:
        return [clause]


def containTautology(clause):
    if type(clause) == str or len(clause) <= 1:
        return False
    else:
        for item in clause:
            if changeNegation(item) in clause:
                return True
    return False

def sublist(l1, l2):

    for element in l1:
        if not element in l2:
            return False
    return True


def unique(clauses):
    if type(clauses) == str:
        return clauses
    if len(clauses) == 0:
        return clauses
    ret = []

    ElementList = list(set([str(element) for element in clauses]))

    for element2 in ElementList:
        if '[' in element2:
            ret.append(eval(element2))
        else:
            ret.append(element2)
    return ret

def combine(op, elements):

    if len(elements) == 0:
        return elements
    elif len(elements) == 1:
        return elements[0]
    elif op == 'and':
        return ['and'] + elements
    elif op == 'or':
        return ['or'] + elements


def findvar1(d):
    if (d.find('(') != -1 and d.find(')') != -1):
        start = d.find('(')
        end = d.find(')')
        if (d.find(')', end + 1) != -1):
            end = d.find(')', end + 1)
        d_temp = d[:start]
        var = d[start + 1:end]
        if (d.find(',') != -1):
            inter = d.find(',')
            var1 = d[start + 1:inter]
            var2 = d[inter + 1:end]
            return (d_temp, var1, var2)
        else:
            return (d_temp, var, None)
    else:
        return (d, None, None)


def findvar2(d):
    if (d[1].find('(') != -1 and d[1].find(')') != -1):
        start = d[1].find('(')
        end = d[1].find(')')
        if (d[1].find(')', end + 1) != -1):
            end = d[1].find(')', end + 1)
        d_temp = ['not', d[1][:start]]
        var = d[1][start + 1:end]
        if (d[1].find(',') != -1):
            inter = d[1].find(',')
            var1 = d[1][start + 1:inter]
            var2 = d[1][inter + 1:end]
            return (d_temp, var1, var2)
        else:
            return (d_temp, var, None)
    else:
        return (d, None, None)


def changevar1(d, var='£', var1='£', var2='£'):
    d_temp = []
    for w in d:
        if (len(w) == 2):
            start1 = w[1].find(var1)
            start2 = w[1].find(var2)
            w_temp = w
            if (start1 != -1 and start2 == -1):
                w_temp = ['not', w[1].replace(var1, var)]
            if (start2 != -1 and start1 == -1):
                w_temp = ['not', w[1].replace(var2, var)]
            if (start1 != -1 and start2 != -1):
                w_temp = w[1].replace(var1, var)
                w_temp = ['not', w_temp.replace(var2, var)]
            d_temp.append(w_temp)

        else:
            start1 = w.find(var1)
            start2 = w.find(var2)
            w_temp = w
            if (start1 != -1 and start2 == -1):
                w_temp = w.replace(var1, var)
            if (start2 != -1 and start1 == -1):
                w_temp = w.replace(var2, var)
            if (start1 != -1 and start2 != -1):
                w_temp = w.replace(var1, var)
                w_temp = w_temp.replace(var2, var)
            d_temp.append(w_temp)

    return (d_temp)


def changevar2(d, sub1, sub2, var_i1, var_i2, var_j1, var_j2):
    d_temp = []
    for w in d:
        w_temp = w
        if (len(w) == 2):
            pos11 = w[1].find(var_i1)
            pos21 = w[1].find(var_j1)
            pos12 = w[1].find(var_i2)
            pos22 = w[1].find(var_j2)

            if (pos11 != -1):
                w = ['not', w[1].replace(var_i1, sub1)]
            if (pos12 != -1):
                w = ['not', w[1].replace(var_i2, sub2)]
            if (pos21 != -1):
                w = ['not', w[1].replace(var_j1, sub1)]
            if (pos22 != -1):
                w = ['not', w[1].replace(var_j2, sub2)]
            d_temp.append(w)

        else:
            pos11 = w.find(var_i1)
            pos21 = w.find(var_j1)
            pos12 = w.find(var_i2)
            pos22 = w.find(var_j2)

            if (pos11 != -1):
                w = w.replace(var_i1, sub1)
            if (pos12 != -1):
                w = w.replace(var_i2, sub2)
            if (pos21 != -1):
                w = w.replace(var_j1, sub1)
            if (pos22 != -1):
                w = w.replace(var_j2, sub2)
            d_temp.append(w)

    return (d_temp)


def Resolve(ci, cj):
    clauses = []
    i, j, k, l, m, n, o, p = 100, 200, 300, 400, 500, 600, 700, 800

    for di in disCombine('or', ci):
        if (len(di) == 2):
            di_temp, var_i1, var_i2 = findvar2(di)
        else:
            di_temp, var_i1, var_i2 = findvar1(di)

        for dj in disCombine('or', cj):
            if (len(dj) == 2):
                dj_temp, var_j1, var_j2 = findvar2(dj)
            else:
                dj_temp, var_j1, var_j2 = findvar1(dj)
            i, j, k, l, m, n, o, p = i + 1, j + 1, k + 1, l + 1, m + 1, n + 1, o + 1, p + 1

            if (di_temp == changeNegation(dj_temp) or changeNegation(di_temp) == dj_temp):

                if (var_i1 in Variables and var_j1 in Variables and var_i2 == var_j2 == None):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar1(dNew, str(i), var_i1, var_j1)
                    Variables.append(str(i))
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 in Variables and var_j1 in Constants and var_i2 == var_j2 == None):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar1(dNew, var_j1, var_i1)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 in Constants and var_j1 in Variables and var_i2 == var_j2 == None):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar1(dNew, var_i1, var_j1)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_j1 != None and var_i1[:4] in Functions and var_j1 in Variables and var_i2 == var_j2 == None):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar1(dNew, var_i1, var_j1)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_j1 != None and var_j1[:4] in Functions and var_i1 in Variables and var_i2 == var_j2 == None):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar1(dNew, var_j1, var_i1)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 and var_i2 and var_j1 and var_j2 in Variables):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, str(k), str(j), var_i1, var_i2, var_j1, var_j2)
                    Variables.append(k)
                    Variables.append(j)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if ((var_i1 and var_i2 in Variables) and (var_j1 and var_j2 in Constants)):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_j1, var_j2, var_i1, var_i2, var_j1, var_j2)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if ((var_j1 and var_j2 in Variables) and (var_i1 and var_i2 in Constants)):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_i1, var_i2, var_i1, var_i2, var_j1, var_j2)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if ((var_i1 and var_j1 in Variables) and (var_i2 == var_j2 in Constants)):
                    # print(13)
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, str(l), var_j2, var_i1, var_i2, var_j1, var_j2)
                    Variables.append(str(l))
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 != None and var_i1[
                                       :4] in Functions and var_i2 in Constants and var_j1 in Variables and var_j2 in Variables):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_i1, var_i2, var_i1, var_i2, var_j1, var_j2)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 != None and var_i1[
                                       :4] in Functions and var_i2 in Variables and var_j1 in Variables and var_j2 in Variables):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_i1, str(m), var_i1, var_i2, var_j1, var_j2)
                    Variables.append(str(m))
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_j1 != None and var_j1[
                                       :4] in Functions and var_i2 == var_j2 and var_i1 in Variables and var_j2 in Constants):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_i1, str(n), var_i1, var_i2, var_j1, var_j2)
                    Variables.append(str(n))
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                if (var_i1 != None and var_i1[
                                       :4] in Functions and var_i2 == var_j2 and var_j1 in Variables and var_j2 in Constants):
                    diNew = disCombine('or', ci)
                    diNew.remove(di)
                    djNew = disCombine('or', cj)
                    djNew.remove(dj)
                    dNew = diNew + djNew
                    dNew = changevar2(dNew, var_i1, str(o), var_i1, var_i2, var_j1, var_j2)
                    Variables.append(o)
                    dNew = unique(dNew)
                    toAddD = combine('or', dNew)
                    clauses.append(toAddD)

                else:
                    if di == changeNegation(dj) or changeNegation(di) == dj:
                        diNew = disCombine('or', ci)
                        diNew.remove(di)
                        djNew = disCombine('or', cj)
                        djNew.remove(dj)
                        dNew = diNew + djNew
                        dNew = unique(dNew)
                        toAddD = combine('or', dNew)
                        clauses.append(toAddD)

    return (clauses)



def Resolution(clauses, alpha=0):
    newList = []
    i = 0
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(1, n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = Resolve(ci, cj)
            i = i + 1
            if [] in resolvents:
                return 'No'
            for tempCR in resolvents:
                if not tempCR in newList:
                    newList.append(tempCR)
        newList = [cc for cc in newList if not containTautology(cc)]

        if sublist(newList, clauses):
            return 'Yes'
        for cc in newList:
            if not cc in clauses:
                clauses.append(cc)
#Input                
program_name = sys.argv[0]
argument = sys.argv[1]
count = len(argument)
f = open(argument)
f = f.readlines()
nb_lines = len(f)

Predicates=f[0].split()[1:]
Variables=f[1].split()[1:]
Constants=f[2].split()[1:]
Functions=f[3].split()[1:]
Clauses=[]
for i in range(5,nb_lines) :
    line=f[i].split()
    Clauses.append(line)

for i in range(0,len(Clauses)):
    for j in range(0,len(Clauses[i])):
         if(Clauses[i][j][0]=='!'):
            Clauses[i][j]=['not', Clauses[i][j][1:len(Clauses[i][j])]]
    if(len(Clauses[i])>1):
        Clauses[i].insert(0,'or')
    else:
        Clauses[i]=Clauses[i][0]

Clauses.insert(0,'and')
print(Resolution(Clauses))
