import requests as r
import hashlib as hs
import time as t
import pandas as pd

# Variáveis Auxiliares
chavePublica = "367a1435053cb1f2d913aff85d813068"
chavePrivada = "a8f6ab2ccada0839cbe25bf5cbbb59c72058a95a"
ts = str(int(t.time()))
stringToHash = ts + chavePrivada + chavePublica
qtdRegistros: int = 100
skipRegistros = 0
contagem = -1
total = -1

# DataSctructures
herois = []

# Monta a Requisição
urlBase = "https://gateway.marvel.com:443/v1/public/characters?"
hashMd5 = hs.md5(stringToHash.encode("utf-8")).hexdigest()
urlHash = urlBase + "ts=" + ts + "&apikey=" + chavePublica + "&hash=" + hashMd5

# Loop de paginação
print("Percentual de Conclusão:")
print("0.0%")
while contagem != 0:
    urlRequest = urlHash + "&limit=" + str(qtdRegistros) + "&offset=" + str(skipRegistros)

    personagens = r.get(urlRequest).json()
    contagem = personagens["data"]["count"]
    total = personagens["data"]["total"]
    skipRegistros = skipRegistros + contagem

    percentual = round(skipRegistros / (total / 100), 1)

    if percentual < 100.0:
        print(str(percentual) + "%")

    # Loop de Heróis
    for personagem in personagens["data"]["results"]:
        heroi = {"id": personagem["id"],
                 "name": personagem["name"],
                 "description": personagem["description"],
                 "comics": personagem["comics"]["available"],
                 "series": personagem["series"]["available"],
                 "stories": personagem["stories"]["available"],
                 "events": personagem["events"]["available"]}
        herois.append(heroi)

# Monta o DataFrame
resultadoFinal = pd.DataFrame(herois)
print("Resultado:")
print(resultadoFinal)
