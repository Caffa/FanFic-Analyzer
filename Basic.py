import urllib2 as ur #might need to change to urllib2
import bs4 as bs
import string
import numpy as np
import pandas as pd

def parsesumm(listofall):
    ratingLs = []
    languageLs = []
    genreLs = []
    chaptersLs = []
    wordsLs = []
    reviewsLs = []
    favsLs = []
    followsLs = []
    updatedLs = []
    publishedLs = []
    charactersLs = []
    completeLs = []
    summaryLs = []
    for i in listofall:
        a = str(i)
        b = a[31:-13] #string without front tag
        endSummary = b.find('<div class')
        summary = b[:endSummary] ##########################
        #print b
        startRating = b.find('Rated:')
        aChunkOfInfo = b[startRating+7:]
        ########################
        #print aChunkOfInfo 
        c = string.split(str(aChunkOfInfo), ' - ')
        #print c
        rating = c[0]
        language = c[1]
        genre = c[2] ##### split?
        d = string.split(str(c[2]), '/')
        chapters = c[3][10:] #assume not in multiple numbers
        wordsholder = c[4][7:]
        words = string.replace(wordsholder, ',', '')
        reviewsholder = c[5][9:]
        reviews = string.replace(reviewsholder, ',', '')
        favsholder = c[6][6:]
        favs = string.replace(favsholder, ',', '')
        followsholder = c[7][9:]
        follows = string.replace(followsholder, ',', '')
        updated = c[8][40:-7] #c[8][28:-17] for the random number (time stamp?)
        published = c[8][42:-7]
        characters = c[9]
        complete = False
        if len(c) == 12:
            if c[11] == 'Complet':
                complete = True
        ########################
        #list appends
        summaryLs.append(summary)
        ratingLs.append(rating)
        languageLs.append(language)
        chaptersLs.append(chapters)
        wordsLs.append(words)
        reviewsLs.append(reviews)
        favsLs.append(favs)
        followsLs.append(follows)
        updatedLs.append(updated)
        publishedLs.append(published)
        charactersLs.append(characters)
        completeLs.append(complete)
        genreLs.append(genre)

    return (ratingLs, languageLs, genreLs, chaptersLs, wordsLs, reviewsLs,
    favsLs, followsLs, updatedLs, publishedLs, charactersLs, completeLs, summaryLs)

def getdata(soup):
    titlesLs = []
    idsLs = []
    #lastchapLs = []
    for link in soup.find_all('a'):
        #print link
        b = (link.get('href'))
        #print(b)
        a = string.strip(b, '/')
        c = string.rsplit(a, '/')
        if c[0] == 's':
            #these are stories
            story = c
            if story[2] == '1':
                storytitle = string.replace(story[3], '-', ' ')
                storyid = story[1]
                #print storytitle
                titlesLs.append(storytitle)
                idsLs.append(storyid)
            #else:
            #    lastchapter = story[2]
            #    lastchapLs.append(lastchapter)
    return (titlesLs, idsLs) #, lastchapLs

def getdatatwo(soup):
    alldata = []
    for i in soup.find_all("div", class_="z-indent z-padtop"):
        alldata.append(i)
    (ratingLs, languageLs, genreLs, chaptersLs, wordsLs, reviewsLs,
    favsLs, followsLs, updatedLs, publishedLs, charactersLs, completeLs, summaryLs) = parsesumm(alldata)
    
    return (ratingLs, languageLs, genreLs, chaptersLs, wordsLs, reviewsLs,
    favsLs, followsLs, updatedLs, publishedLs, charactersLs, completeLs, summaryLs)
    



def finalgrab(times):
    titlesLsTotal = []
    idsLsTotal = []
    #lastchapLsTotal = []
    ratingLsTotal = []
    languageLsTotal = []
    genreLsTotal = []
    chaptersLsTotal = []
    wordsLsTotal = []
    reviewsLsTotal = []
    favsLsTotal = []
    followsLsTotal = []
    updatedLsTotal = []
    publishedLsTotal = []
    charactersLsTotal = []
    completeLsTotal = []
    summaryLsTotal = []
    for i in range(times):
        a = "https://www.fanfiction.net/anime/Naruto/?&srt=5&r=10"
        if i == 0:
            c = a
        else:
            c = a + "&p=" + str(i+2)
        sauce = ur.urlopen(c).read()
        soup = bs.BeautifulSoup(sauce,'lxml')
        titlesLs, idsLs = getdata(soup)
        (ratingLs, languageLs, genreLs, chaptersLs, wordsLs, reviewsLs,
         favsLs, followsLs, updatedLs, publishedLs, charactersLs, completeLs, summaryLs) = getdatatwo(soup)
        titlesLsTotal.extend(titlesLs)
        summaryLsTotal.extend(summaryLs)
        idsLsTotal.extend(idsLs)
        #lastchapLsTotal.extend(lastchapLs)
        ratingLsTotal.extend(ratingLs)
        languageLsTotal.extend(languageLs)
        genreLsTotal.extend(genreLs)
        chaptersLsTotal.extend(chaptersLs)
        wordsLsTotal.extend(wordsLs)
        reviewsLsTotal.extend(reviewsLs)
        favsLsTotal.extend(favsLs)
        followsLsTotal.extend(followsLs)
        updatedLsTotal.extend(updatedLs)
        publishedLsTotal.extend(publishedLs)
        charactersLsTotal.extend(charactersLs)
        completeLsTotal.extend(completeLs)
        #fix it so all are in the same
    return (titlesLsTotal, idsLsTotal, ratingLsTotal,
            languageLsTotal, genreLsTotal,
            chaptersLsTotal, wordsLsTotal, reviewsLsTotal,
            favsLsTotal, followsLsTotal, updatedLsTotal, publishedLsTotal, charactersLsTotal, completeLsTotal, summaryLsTotal)


#code
(titlesLsTotal, idsLsTotal, ratingLsTotal,
 languageLsTotal, genreLsTotal,
 chaptersLsTotal, wordsLsTotal, reviewsLsTotal,
 favsLsTotal, followsLsTotal, updatedLsTotal, 
 publishedLsTotal, charactersLsTotal, completeLsTotal, summaryLsTotal) = finalgrab(3)


data = pd.DataFrame({'titles' : titlesLsTotal, 'ids' : idsLsTotal,
                     'rating' : ratingLsTotal,'language' : languageLsTotal,
                     'genre' : genreLsTotal,
                     'chapters' : chaptersLsTotal,'words' : wordsLsTotal,
                     'reviews' : reviewsLsTotal,'favs' : favsLsTotal,
                     'follows' : followsLsTotal,'updated' : updatedLsTotal,
                     'published' : publishedLsTotal,'characters' : charactersLsTotal, 
                     'completed' : completeLsTotal, 'summary' : summaryLsTotal
                     })

#pandas.DataFrame({k : pandas.Series(v) for k, v in datapre.iteritems()})


#data = pd.DataFrame({'titlesLsTotal' : titlesLsTotal, 'followsLsTotal' : followsLsTotal,'updatedLsTotal' : updatedLsTotal})
print data
#data.describe()
