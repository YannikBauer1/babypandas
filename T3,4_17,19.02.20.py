import datetime

with open('resultados-legislativas.csv') as fd:
    lines = fd.readlines()

titles = lines[0].strip().split(',')
print("Titulos das colunas: " + repr(titles))
lines = lines[1:]
print("Exemplo de uma linha: " + repr(lines[5]))
striped_lines = [line.strip() for line in lines]
print("Mesma linha depois do strip(): " + repr(striped_lines[5]))
split_lines = [line.split(',') for line in striped_lines]
print("Mesma linha depois do split(): " + repr(split_lines[5]))

def convert_date(date_as_str):
    return datetime.datetime.strptime(date_as_str,"%Y-%m-%d")

def convert_data(line):
    return [
        int(line[0]),
        line[1],
        line[2],
        convert_date(line[3]),
        line[4],
        int(line[5]),
        float(line[6]),
        int(line[7])
    ]

parsed_lines = [convert_data(line) for line in split_lines] # TODO: converter strings nos tipos correctos

print("Mesma linha depois da conversão de tipos: " + repr(parsed_lines[5]))


votos_ps = [entrada for entrada in parsed_lines if entrada[4] == "PS"]

num_votos_ps = sum([entrada[5] for entrada in votos_ps])

print("Número total de votos no PS registados nos nossos dados: {0}".format(num_votos_ps))

def chave_num_votos(entrada):
    return entrada[5]

print("""
Pergunta: Qual foram as três eleições para a assembleia da républica aonde foram registados
mais votos num só partido em Lisboa? Em que ano, quantos votos, em que partido?
""")

votos_lisboa = [entrada for entrada in parsed_lines if entrada[1].lower() == 'lisboa']
votos_lisboa_ordenado_por_num_votos = sorted(votos_lisboa, key=chave_num_votos, reverse=True )

resposta = votos_lisboa_ordenado_por_num_votos[0:3]

def votos_str(linha):
    return "Eleição de {0}, com {1} votos no {2}".format(linha[3], linha[5], linha[4])

print("Reposta:")
for linha in resposta:
    print(" - " + votos_str(linha))


print("""
Pergunta: Qual foram as três eleições para a assembleia da républica aonde foram registados
mais votos *no PS* em Lisboa? Em que ano, quantos votos, em que partido?
""")



print("""
Pergunta: Qual foram as três eleições para a assembleia da républica aonde foram registados
mais votos por um só partido (no país inteiro)? Em que ano, quantos votos, em que partido?
""")



# TODO: responder

def group_by_data_partido(data):
    def chave_data_partido(entrada):
        return (entrada[3], entrada[4])

    ordenado_por_data_partido = sorted(data, key=chave_data_partido)


    return None # TODO finish


def remove_duplicates_data(data):

    return None # TODO finish



print("ok")