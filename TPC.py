import babypandas as pd

data = pd.read_csv('resultados-legislativas.csv', colparser={"codigo": int,"data": pd.convert_date,"num_votos": int,"perc_votos": float,"mandatos": int})

resposta=data\
    .group_by(["data","partido"],{"num_votos":sum})\
    .sort_values(['data', 'num_votos'], ascending=[True,False])\
    .drop_duplicates(['data'])\
    .sort_values(["num_votos"], ascending=[False])

print(resposta)


