import requests
import concurrent.futures
import db

def todos_monstros():
    requisicao = session.get(url)
    return requisicao.json()

def detalhes_monstros(monstro):
    url = f'https://www.dnd5eapi.co{monstro['url']}'
    deserializer = session.get(url).json()
    return [deserializer['name'],
     deserializer['hit_points'],
     deserializer['challenge_rating']
     ]

global session
session = requests.Session()
url = 'https://www.dnd5eapi.co/api/monsters'
deserializer = todos_monstros()['results']
with concurrent.futures.ThreadPoolExecutor(max_workers= 10) as executor:
    resultado = executor.map(detalhes_monstros, deserializer)

print(resultado)
conn = db.criar_conexao()
cursor = conn.cursor()
sql = 'SELECT * FROM monstros_dnd'
cursor.execute(sql)
resultado_banco = cursor.fetchall()
print(resultado_banco)
cursor.close()
conn.close()


