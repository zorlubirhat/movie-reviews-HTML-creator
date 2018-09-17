import os
from collections import defaultdict

# STAGE 1


def readdatafile(file):

    infile = open(file, "r")
    data = defaultdict(lambda: defaultdict())
    for line in infile.readlines():
        line = line.rstrip("\n")
        lines = line.split("\t")
        data[int(lines[0])][lines[1]] = lines[2]
    return data

data = readdatafile("u.data")


def readfile(file):

    infile = open(file, "r")
    info = dict()
    for line in infile.readlines():
        line = line.rstrip("\n")
        lines = line.split("|")
        info[int(lines[1])] = lines[0]
    return info

genre = readfile("u.genre")


def readfile2(file):

    infile = open(file, "r", encoding='iso-8859-1')
    info = dict()
    for line in infile.readlines():
        line = line.rstrip("\n")
        lines = line.split("|")
        info[int(lines[0])] = lines[1:]
    return info

item = readfile2("u.item")
user = readfile2("u.user")


def readfile3(file):

    infile = open(file, "r")
    info = dict()
    for line in infile.readlines():
        line = line.rstrip("\n")
        lines = line.split("|")
        info[int(lines[0])] = lines[1]
    return info

occupation = readfile3("u.occupation")


def readtxt(file):

    os.chdir(file)
    movie_title = []
    movie_review = []
    for film in os.listdir(os.getcwd()):
        f = open(film, "r", encoding='iso-8859-1')
        review = []
        for line in f.readlines():
            line = line.rstrip("\n")
            review.append(line)
            title = str(review[0]).split(" (")
        review.pop(0)
        movie_review.append(review)
        movie_title.append(title[0].lower())
    os.chdir("..")
    return movie_title, movie_review

movie = readtxt("film")
movie_title = movie[0]
movie_review = movie[1]


def findMovie(givenlist):

    movie_id = []
    for i in givenlist:
        for j in item:
            a = str(item[j][0]).split(" (")[0]
            if i == a.lower():
                movie_id.append(j)
    return movie_id

movie_id = sorted(findMovie(movie_title))
movie_name = [str(item[mov][0]).split(" (")[0] for mov in movie_id]


def createReviewTxt():

    out_file = open("review.txt", "w")
    try:
        for i in item:
            if i in movie_id:
                out_file.write("{} {} is found in folder.\n".format(i, str(item[i][0]).split(" (")[0]))
            else:
                out_file.write("{} {} is not found in folder. Look at {}\n".format(i, str(item[i][0]).split(" (")[0], item[i][2]))
    except:
        pass
    out_file.close()

createReviewTxt()


def findGenre(givenList):

    genres = list()
    for i in givenList:
        a = -1
        gen = []
        for j in item[i][3:]:
            a += 1
            if int(j) == 1:
                gen.append(genre[a])
        genres.append(gen)
    return genres

movie_genre = findGenre(movie_id)
movie_link = [str(item[x][2]) for x in movie_id]


def findUser(givenlist):

    rate = defaultdict(lambda: defaultdict())
    for z in givenlist:
        for x in data.keys():
            for y in data[x].items():
                if z == int(y[0]):
                    rate[z][x] = y[1]
                else:
                    pass
    return rate

usering = findUser(movie_id)


def findUsersInfo(givendict):
    users = []
    for k, v in givendict.items():
        user2 = []
        user2.append(k)
        for z, x in v.items():
            user2.append(z)
            user2.append(x)
        users.append(user2)
    return users

rateuser = sorted(findUsersInfo(usering))


def findRates(givenlist):
    rates = []
    for z in givenlist:
        rat = []
        rat.append(z[0])
        for x in z:
            b = z[2::2]
            c = z[1::2]
            count = 0
            for y in b:
                count += int(y)
        rat.append(count)
        rat.append(len(c))
        rates.append(rat)
    return rates

Rates = findRates(rateuser)

#os.mkdir("filmList")
os.chdir("filmList")
for i in range(len(movie_name)):
    file = open("{}.html".format(movie_id[i]), "w")
    string = "<html><head><title>" + movie_name[i] + "</title></head>"
    file.write(string)
    string2 = """<body><font face="Times New Roman" font size="6" color="red"<b>""" + movie_name[i] + """</b></font><br>"""
    file.write(string2)
    string3 = """<b>Genre: </b>"""
    file.write(string3)
    for x in movie_genre[i]:
        string4 = x + " "
        file.write(string4)
    string5 = """<br>"""
    file.write(string5)
    string6 = "<b>IMDB Link: </b><a href=" + movie_link[i] + ">" + movie_name[i] + "</a><br>"
    file.write(string6)
    string7 = """<font face="Times New Roman" font size="4" color="black"><b>Review: </b><br>"""
    file.write(string7)
    for y in movie_review[i]:
        string8 = y
        file.write(string8)
    string9 = "</font><br><br>"
    file.write(string9)
    string10 = "<b>Total User: </b>"
    file.write(string10)
    for w in Rates:
        if w[0] == movie_id[i]:
            string11 = str(w[2])
            string12 = " <b>/ Total Rate: </b>"
            string13 = str(int(w[1]) / int(w[2]))
            file.write(string11)
            file.write(string12)
            file.write(string13)
    string14 = "<br><br><b>User who rate the film: </b><br>"
    file.write(string14)
    c = 1
    d = 2
    for a in range(len(rateuser[i][1::2])):
        if Rates[i][0] == rateuser[i][0]:
            string14 = "<b>User: </b>" + str(rateuser[i][c])
            string15 = "<b> Rate: </b>" + str(rateuser[i][d])
            string16 = "<br><b>User Detail: </b>"
            string17 = "<b>Age: </b>" + str(user[rateuser[i][c]][0])
            string18 = "<b> Gender: </b>" + str(user[rateuser[i][c]][1])
            string19 = "<b> Occupation: </b>" + str(occupation[int(user[rateuser[i][c]][2])])
            string20 = "<b> Zip Code: </b>" + str(user[rateuser[i][c]][3]) + "<br>"
            c += 2
            d += 2
            file.write(string14)
            file.write(string15)
            file.write(string16)
            file.write(string17)
            file.write(string18)
            file.write(string19)
            file.write(string20)
    i += 1
os.chdir("..")


def readStopWords(text):

    infile = open(text, "r", encoding="utf-8")
    stopWords = set()
    for line in infile.readlines():
        line = line.strip("\n")
        stopWords.add(line)
    return stopWords

stopword = readStopWords("stopwords.txt")

unknown = set()
Action = set()
Adventure = set()
Animation = set()
Childrens = set()
Comedy = set()
Crime = set()
Documentary = set()
Drama = set()
Fantasy = set()
FilmNoir = set()
Horror = set()
Musical = set()
Mystery = set()
Romance = set()
SciFi = set()
Thriller = set()
War = set()
Western = set()


for x in movie_review:
    ind = movie_review.index(x)
    for y in x:
        z = str(y).lower().split(" ")
        for w in z:
            for genres in movie_genre[ind]:
                if genres == 'unknown':
                    if w in stopword:
                        pass
                    else:
                        unknown.add(w)
                if genres == 'Action':
                    if w in stopword:
                        pass
                    else:
                        Action.add(w)
                if genres == 'Adventure':
                    if w in stopword:
                        pass
                    else:
                        Adventure.add(w)
                if genres == 'Animation':
                    if w in stopword:
                        pass
                    else:
                        Animation.add(w)
                if genres == "Children's":
                    if w in stopword:
                        pass
                    else:
                        Childrens.add(w)
                if genres == 'Comedy':
                    if w in stopword:
                        pass
                    else:
                        Comedy.add(w)
                if genres == 'Crime':
                    if w in stopword:
                        pass
                    else:
                        Crime.add(w)
                if genres == 'Documentary':
                    if w in stopword:
                        pass
                    else:
                        Documentary.add(w)
                if genres == 'Drama':
                    if w in stopword:
                        pass
                    else:
                        Drama.add(w)
                if genres == 'Fantasy':
                    if w in stopword:
                        pass
                    else:
                        Fantasy.add(w)
                if genres == 'Film-Noir':
                    if w in stopword:
                        pass
                    else:
                        FilmNoir.add(w)
                if genres == 'Horror':
                    if w in stopword:
                        pass
                    else:
                        Horror.add(w)
                if genres == 'Musical':
                    if w in stopword:
                        pass
                    else:
                        Musical.add(w)
                if genres == 'Mystery':
                    if w in stopword:
                        pass
                    else:
                        Mystery.add(w)
                if genres == 'Romance':
                    if w in stopword:
                        pass
                    else:
                        Romance.add(w)
                if genres == 'Sci-Fi':
                    if w in stopword:
                        pass
                    else:
                        SciFi.add(w)
                if genres == 'Thriller':
                    if w in stopword:
                        pass
                    else:
                        Thriller.add(w)
                if genres == 'War':
                    if w in stopword:
                        pass
                    else:
                        War.add(w)
                if genres == 'Western':
                    if w in stopword:
                        pass
                    else:
                        Western.add(w)

movie2 = readtxt("filmGuess")
movie_title2 = movie2[0]
movie_review2 = movie2[1]


outfile = open("filmGenre.txt", "w")
aaa = "Guess Genres of Movie based on Movies\n"
for xn in movie_review2:
    ind2 = movie_review2.index(xn)
    filmset = set()
    aaa += str(movie_title2[ind2]).upper() + " : "
    for yn in xn:
        zn = str(yn).lower().split(" ")
        for wn in zn:
            if wn in stopword:
                pass
            else:
                filmset.add(wn)
                out3 = ""
                if len(filmset.intersection(unknown)) > 20:
                    out3 += "unknown "
                if len(filmset.intersection(Action)) > 20:
                    out3 += "Action "
                if len(filmset.intersection(Adventure)) > 20:
                    out3 += "Adventure "
                if len(filmset.intersection(Animation)) > 20:
                    out3 += "Animation "
                if len(filmset.intersection(Childrens)) > 20:
                    out3 += "Children's "
                if len(filmset.intersection(Comedy)) > 20:
                    out3 += "Comedy "
                if len(filmset.intersection(Crime)) > 20:
                    out3 += "Crime "
                if len(filmset.intersection(Documentary)) > 20:
                    out3 += "Documentary "
                if len(filmset.intersection(Drama)) > 20:
                    out3 += "Drama "
                if len(filmset.intersection(Fantasy)) > 20:
                    out3 += "Fantasy "
                if len(filmset.intersection(FilmNoir)) > 20:
                    out3 += "Film-Noir "
                if len(filmset.intersection(Horror)) > 20:
                    out3 += "Horror "
                if len(filmset.intersection(Musical)) > 20:
                    out3 += "Musical "
                if len(filmset.intersection(Mystery)) > 20:
                    out3 += "Mystery "
                if len(filmset.intersection(Romance)) > 20:
                    out3 += "Romance "
                if len(filmset.intersection(SciFi)) > 20:
                    out3 += "Sci-Fi "
                if len(filmset.intersection(Thriller)) > 20:
                    out3 += "Thriller "
                if len(filmset.intersection(War)) > 20:
                    out3 += "War "
                if len(filmset.intersection(Western)) > 20:
                    out3 += "Western "
    aaa += out3
    aaa += "\n"
outfile.write(aaa)
outfile.close()
