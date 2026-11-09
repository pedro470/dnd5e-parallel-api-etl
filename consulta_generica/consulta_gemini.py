import requests


url = "https://www.dnd5eapi.co/api/monsters"
print("Iniciando a caçada...")

session = requests.Session()
response = session.get(url)

if response.status_code == 200:
    dados = response.json()
    # TRUQUE DE MESTRE: Slice na lista [:5]
    # Isso pega só do índice 0 ao 4. O resto ele ignora.
    monstros_para_processar = dados['results'][:5] 

    print(f"Processando amostra de {len(monstros_para_processar)} monstros...")

    for monstro in monstros_para_processar:
        print(f"--> Investigando: {monstro['name']}")
        
        # Pega a URL relativa e monta a completa
        url_detalhe = "https://www.dnd5eapi.co" + monstro['url']
        
        resp_detalhe = session.get(url_detalhe)
        
        if resp_detalhe.status_code == 200:
            info = resp_detalhe.json()
            # Vamos pegar só o que importa pro nosso "Banco de Dados" futuro
            hp = info.get('hit_points', 0) # .get evita erro se não tiver HP
            cr = info.get('challenge_rating', 0)
            tipo = info.get('type', 'desconhecido')
            
            print(f"STATUS: HP={hp} | CR={cr} | Tipo={tipo}")
        else:
            print("Falha ao obter detalhes.")
else:
    print("A API principal falhou.")