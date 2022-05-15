from collections import Counter


def initial_key(F):
    W = []
    filedata = []
    for idx, val in enumerate(F):
        cnt = Counter()
        for line in open('./doc/'+F[idx], 'r'):
            word_list = line.replace(',', '').replace('\'', '').replace('.', '').lower().split()
            for word in word_list:
                cnt[word] += 1 
        filedata.append([val, cnt]) 

    for idx, val in enumerate(filedata):
        allwords = []  
        for value in val[1].most_common(200): 
            if value not in allwords:
                allwords.append(value)
        W.append(allwords)
    return W

