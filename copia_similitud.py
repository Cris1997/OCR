

def stop_scraper(mes, stopwords):
    tknzr = TweetTokenizer()
    mesTK = []
    for c in tknzr.tokenize(mes):
        if c not in stopwords:
            mesTK.append(c)
    return mesTK

def entity_ref_extractor(Mess, Refer, stop_words):
    spanish_stopwords = stopwords.words('spanish')
    spanish_stopwords.extend(string.punctuation)
    stop_words.extend(spanish_stopwords)
    References = []
    Distances = []
    disArray = []
    # listind = []
    targlen = []
    mesTK = stop_scraper(Mess, stop_words)
    if mesTK == []:
        return []
    for z in range(len(Refer)):
        refTK = stop_scraper(Refer[z].lower(), stop_words)
        # print("REFTK:",refTK)
        refblank = ['X' for _ in range(len(mesTK)-1)]
        # print("refCon:",refblank )
        refCon = copy.copy(refblank)
        refCon.extend(refTK)
        refCon.extend(refblank)
        # print("refCon:",refCon)
        disTotal = len(mesTK)
        targlen.append(len(refTK))
        refref = []
        distan = []
        distref = []
        # print(len(refTK)+len(mesTK)-1)
        for i in range(len(refTK)+len(mesTK)-1):
            distan = []
            for j in range(len(mesTK)):
                # print("Compara: ",mesTK[j],"con :", refCon[i:(i+len(mesTK))][j]) 
                e_distance = (edit_distance(mesTK[j],refCon[i:(i+len(mesTK))][j]))
                m_len = max(len(mesTK[j]),len(refCon[i:(i+len(mesTK))][j]))
                distan.append(e_distance / m_len )
            # print(distan)
                
            norm = 1
            disT = 10
            base = 0
            for q in range(len(distan)):
                if distan[q] < 0.3:
                    base = base + distan[q]
                    norm = norm+1
                    disT = base
            if disT != 0:
                disTemp = disT/norm
            else:
                disTemp = 0
            # print("disTemp",disTemp)
            # print("disTotal",disTotal)
            if disTotal > disTemp:
                # print("entra")
                distref = distan
                refref = refCon[i:i+len(mesTK)]
                disTotal = disTemp
        Distances.append(distref)
        disArray.append(disTotal) 
        References.append(refref)
    output = []
    sortindex = sorted(range(len(disArray)),key=lambda x: disArray[x])
    # print("Disarray:",disArray)
    sortdisArray = sorted(disArray)
    # print("SortDisarrya:", sortdisArray)
    refmatch = []
    targmatch = []
    posible = []
    for fg in range(len(sortdisArray)):
        if (sortdisArray[fg]) < 1:
            matcher = sum(di < 0.2 for di in Distances[sortindex[fg]])
            if (min(Distances[sortindex[fg]]) < 0.2):
                posible.append(Refer[sortindex[fg]])
                refmatch.append(matcher)
                targmatch.append(targlen[sortindex[fg]])
    for ref in range(len(refmatch)):
        if refmatch[ref] == max(refmatch):
            output.append(sortindex[ref])
    # print("GEEE")
    # print(output)
    return output