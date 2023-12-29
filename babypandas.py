########################################################################################################################
#----------------------------------------------------------babypandas--------------------------------------------------#
########################################################################################################################

import datetime as datetime
from operator import itemgetter


class DataFrame:
    def __init__(self, coln, rows):
        self.coln = coln
        self.cols = {coln[i]: i for i in range(len(coln))}
        self.rows = rows

    def __str__(self):  #mostra uma tabela dos 5 primeiras e ultimas linhas
        c = self.coln
        r = self.rows
        size = [[len(str(r[x][index])) for x in range(len(r))] + [len(str(c[index]))] for index in range(len(c))]  #fazer uma lista de listas dos tamanhos das colunas
        size = [max(size[x]) for x in range(len(c))]    #ter o maximo das tamanhos de cada coluna
        first = " ".join([("{0:>" + str(size[x]) + "}").format(str(c[x])) for x in range(len(c))])
        if (len(r)<=10):
            middle=table_lines_str(size,r)
        else:
            first5=table_lines_str(size,r[:20])
            last5 = table_lines_str(size, r[len(r) - 0:])
            points = " ".join([("{0:>" + str(size[x]) + "}").format("...") for x in range(len(c))])
            middle= first5 + "\n" + points + "\n" + last5
        end= "[{0} rows x {1} columns]".format(len(r), len(c))
        table = first + "\n" + middle + "\n\n" + end
        return table

    def iloc(self, i):  #devolve a i-ésima linha
        dic = {x: self.rows[i][self.cols[x]] for x in self.cols}
        return dic

    def apply(self, func):  #aplica uma funcao ao linhas
        l = [func(self.iloc(row)) for row in range(len(self.rows))]
        return l

    def insert(self, key, value, dtypes={}):  #adicionar uma uma nova coluna
        if (type(key)!=str) and (True in [type(key[i])!=str for i in range(len(key))]):
            raise KeyError
        if(type(key)==str):
            key=[key]
            value=[[i] for i in value]
        c = self.coln[:]+key
        r = self.rows[:]
        value = [convert_line(line, key, dtypes) for line in value]  #coverter o value
        r=[r[i]+value[i] for i  in range(len(r))]  #juntar os rows e value
        return DataFrame(c, r)

    def sort_values(self,keys,ascending=[]):  #ordena por coluna ou colunas
        if (type(keys) != str) and (True in [type(keys[i]) != str for i in range(len(keys))]):
            raise KeyError
        if type(keys) == str:
            keys = [keys]
            ascending = [ascending]
        c = self.coln[:]
        r = self.rows[:]
        for i in reversed(range(len(keys))):
            if ascending != [] and ascending != [[]]:
                r = sorted(r, key=itemgetter(self.cols[keys[i]]), reverse= not ascending[i])
            else:
                r = sorted(r, key=itemgetter(self.cols[keys[i]]))
        return DataFrame(c,r)

    def drop_duplicates(self,column):   #tira repetidos das colunas dada
        if (type(column)!=str) and (True in [type(column[i])!=str for i in range(len(column))]):
            raise KeyError
        elif type(column)==str:
            column=[column]
        rows=self.rows[:]
        for c in column:
            rows = sorted(rows, key=itemgetter(self.cols[c]))
            rows = [rows[0]] + [rows[i] for i in range(1, len(rows)) if (rows[i][self.cols[c]]) != (rows[i - 1][self.cols[c]])]
        return DataFrame(self.coln,rows)

    def group_by(self,columns,agg):  #faz um dataframe com as colunas dadas sem repeticao e junta os dados da coluna do agg pelo argumento
        indexes=[self.cols[column] for column in columns]+[self.cols[key] for key in agg]  #lista dos indexes das colunas
        coln=[column for column in self.coln if column in columns or column in agg]
        cols = {coln[i]: i for i in range(len(coln))}
        rows=[[line[i] for i in range(len(line)) if i in indexes] for line in self.rows]  #rows só com os dados da lista
        for i in columns:
            rows=sorted(rows,key=itemgetter(cols[i]))
        new_rows=[]
        help_row=[rows[0]]
        pre=[rows[0][cols[j]] for j in columns]
        for i in range(1,len(rows)):  #compara cada linha com a linha anterior se tem as mesmas entradas nas colunas. Vai dar uma lista de listas em que as linhas com as mesmas entradas nas colunas sao grupados (new_rows)
            current=[rows[i][cols[j]] for j in columns]
            if current==pre:
                help_row.append(rows[i])
            else:
                new_rows.append(help_row)
                help_row=[rows[i]]
                pre=current
        rows=[[line[0][cols[i]] for i in columns] for line in new_rows] #reduce new_rows para os dados sem a coluna de agg e sem repeticao
        for i in agg:
            l=[[line[j][cols[i]] for j in range(len(line))] for line in new_rows] #lista com os rows com entrada só para a coluna de agg
            l=[agg[i](line) for line in l]  #por exemplo sum os dados grupados
            for j in range(len(rows)):
                rows[j].insert(cols[i], l[j])
        return DataFrame(coln,rows)


def table_lines_str(size,rows):
    sol = [[("{0:>" + str(size[x]) + "}").format(str(rows[y][x])) for x in range(len(rows[y]))] for y in range(len(rows))]  #ajustar as entradas para o certo tamanho
    sol = [" ".join(sol[y]) for y in range(len(rows))]  # fazer um str por linha
    sol = "\n".join(sol)
    return sol

def buedavotos(row):
    if row['num_votos'] >= 50000:
        return str(row['num_votos']) + ' são bué'
    else:
        return str(row['num_votos']) + ' são poucos'

def convert_date(data_as_str):
    return datetime.datetime.strptime(data_as_str, "%Y-%m-%d").date()

def convert_data(data, index, coln, colparser):
    if type(coln)==str and coln in colparser:
        return (colparser[coln](data))
    elif coln[index] in colparser:
        return (colparser[coln[index]](data))
    return (data)

def convert_line(line, coln, colparser):
    return [convert_data(line[i], i, coln, colparser) for i in range(len(line))]

def read_csv(filename, colparser={}):
    file = open(filename, encoding="utf8")
    lines = file.readlines()
    lines = [line.strip().split(",") for line in lines]
    coln = lines[0]
    rows = [convert_line(line, coln, colparser) for line in lines[1:]]
    return DataFrame(coln, rows)

#######Tests
###read_csv
#data = read_csv('resultados-legislativas.csv', colparser={"codigo": int,"data": convert_date,"num_votos": int,"perc_votos": float,"mandatos": int})

###__str__
#print(data)

###iloc
#print(data.iloc(0)=={'codigo': 10000, 'nome': 'Aveiro', 'tipo': 'AR', 'data': datetime.date(1975, 4, 25), 'partido': 'PPD', 'num_votos': 141872, 'perc_votos': 42.86, 'mandatos': 7})
#dá True

###apply
#print(data.apply(buedavotos)[0:5]==['141872 são bué', '105098 são bué', '36602 são poucos', '12849 são poucos', '10479 são poucos'])
#dá True

###insert
#print(data.insert("quantos",data.apply(buedavotos)))

###sort_values
#print(data.sort_values(['partido', 'num_votos'], ascending=[True, False]))

###drop_duplicates
#print(data.drop_duplicates(["partido","nome"]))

###group_by
#print(data.group_by(["nome","partido"],{"num_votos":sum}))


#Utiliza o teu babypandas para responder à seguinte pergunta:

#Para cada partido nacional, qual foi o distrito aonde foi registada maior percentagem de votos votos em qualquer legislativa? (E qual foi essa percentagem, e em que ano)

#(e.g. PS - em lisboa em 19xx com xx,x% dos votos)

data = read_csv('resultados-legislativas.csv', colparser={"codigo": int,"data": convert_date,"num_votos": int,"perc_votos": float,"mandatos": int})
data=data.sort_values("perc_votos",False)
#print(data)
data=data.drop_duplicates("partido")
data=data.sort_values("perc_votos",False)
print(data)
