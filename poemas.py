####################################################################################
#-------------------------------Poemas---------------------------------------------#
####################################################################################


###Tarefa 2.1
def remove_punctuation(string):
    newText=""
    for i in string:
        if i.isalpha() or i.isspace():
            newText=newText+i
    return newText
#print(remove_punctuation("""Eu nunca guardei rebanhos, Mas é como se os guardasse.""") == """Eu nunca guardei rebanhos Mas é como se os guardasse""")
#dá True


###Tarefa 2.2
def get_words(string):
    newString=remove_punctuation(string).lower()
    return newString.split()
#print(get_words("""Eu nunca guardei rebanhos, Mas é como se os guardasse.""")==['eu', 'nunca', 'guardei', 'rebanhos', 'mas', 'é', 'como', 'se', 'os', 'guardasse'])
#dá True


###Tarefa 3
def get_words_from_file(data):
    file=open(data,encoding="utf8")
    txt=file.read()
    return get_words(txt)
#print(get_words_from_file("exemplo.txt")==['eu', 'nunca', 'guardei', 'rebanhos', 'mas', 'é', 'como', 'se', 'os', 'guardasse', 'minha', 'alma', 'é', 'como', 'um', 'pastor', 'conhece', 'o', 'vento', 'e', 'o', 'sol', 'e', 'anda', 'pela', 'mão', 'das', 'estações', 'a', 'seguir', 'e', 'a', 'olhar', 'toda', 'a', 'paz', 'da', 'natureza', 'sem', 'gente', 'vem', 'sentarse', 'a', 'meu', 'lado', 'mas', 'eu', 'fico', 'triste', 'como', 'um', 'pôr', 'de', 'sol', 'para', 'a', 'nossa', 'imaginação', 'quando', 'esfria', 'no', 'fundo', 'da', 'planície', 'e', 'se', 'sente', 'a', 'noite', 'entrada', 'como', 'uma', 'borboleta', 'pela', 'janela'])
#dá True


###Tarefa 3.1
l1=[str(i**2) for i in range(1,11)] # = ['1', '4', '9', '16', '25', '36', '49', '64', '81', '100']
l2=["Item #"+str(i) for i in range(1,11)] # = ['Item #1', 'Item #2', 'Item #3', 'Item #4', 'Item #5', 'Item #6', 'Item #7', 'Item #8', 'Item #9', 'Item #10']
l3=[[(i,j) for j in range(10)] for i in range(10)] # = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)], [(1, 0), (1, 1), (1, 2), ...


###Tarefa 3.2
def chave_lista(e):
    return int(e[1])
def count_words(list):
    list.sort()
    sol=[]
    count=0
    pre=list[0]
    for i in list:
        if pre==i:
            count=count+1
        else:
            sol.append((pre,count))
            pre=i
            count=1
    sol.append((pre,count))
    sol=sorted(sol,key=chave_lista,reverse=True)
    return sol
def count_word(list,word):
    l=count_words(list)
    for i in l:
        if word==i[0]:
            return i[1]
    return (0)
#print(count_words(get_words_from_file('exemplo.txt')))


###Tarefa 4
def readPoem(poem):                                                          #retorna um dic com os "titles" e paragrafos
    file = open(poem,encoding="utf8")
    txt = file.read()
    lines=txt.split("\n")
    sol = {}
    title=""
    letra=""
    for i in lines:
        if ("#" in i)==True:
            if title!="":
                sol.update({title:letra})
                letra=""
            title=i[2:]
        else:
            if letra=="":
                letra=i
            else:
                letra=letra+" \n"+i
    return sol
#print(readPoem("guardador.txt"))


###TPC
#print("Quais são as cinco palavras mais usadas nos poemas do Guardador de Rebanhos?:",count_words(get_words_from_file("guardador.txt"))[:5])

#print("Quais são as cinco palavras mais usadas nos poemas do Cancioneiro?:",count_words(get_words_from_file("cancioneiro.txt"))[:5])

def terceiraPergunta(data):
    word=count_words(get_words_from_file(data))[1][0]
    #print(count_words(get_words_from_file(data))[1][0])
    #print(word)
    sol=[]
    for key,value in readPoem(data).items():
        w=get_words(value)
        c=count_word(w,word)
        sol.append([key,c])
    sol=sorted(sol,key=chave_lista,reverse=True)
    return sol
a=terceiraPergunta("guardador.txt")
a=a[0][0]
print(a)
p=readPoem("guardador.txt")
print(p.get(a))
print("Qual é o poema no Guardador de Rebanhos que mais vezes utiliza a palavra mais utilizada no livro inteiro?:",terceiraPergunta("guardador.txt")[0])

print("Qual é o poema no Cancioneiro que mais vezes utiliza a palavra mais utilizada no livro inteiro?:",terceiraPergunta("cancioneiro.txt")[0])
