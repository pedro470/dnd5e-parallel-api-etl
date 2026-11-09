import requests
import concurrent.futures

session = None

def pesquisar_monstro(monstro):
    try:
        print(f"Monstro: {monstro['name']}")
        url_requisitada = f'https://www.dnd5eapi.co{monstro['url']}'
        retorno_monstro = session.get(url_requisitada, timeout=10)
        resultado_normalizado = retorno_monstro.json()
        return {    
            'nome': resultado_normalizado['name'],
            'tipo': resultado_normalizado['type'],
            'nivel_desafio': resultado_normalizado['challenge_rating'],
            'hp': resultado_normalizado['hit_points']
        }
        #print(f'Nome: {resultado_normalizado['name']}, Tipo: {resultado_normalizado['type']}, CR: {resultado_normalizado['challenge_rating']}')
    except Exception as e:
        print(f'Erro ao pesquisar monstro {monstro['name']}: {e}')

def consulta_paralela():
    url = "https://www.dnd5eapi.co/api/monsters"
    print("Iniciando a caçada...")

    global session
    session = requests.Session()

    try:
        response = session.get(url)
        request_bruta = response.json()

        todos_monstros = request_bruta['results']
        if response.status_code == 200:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                resultados = executor.map(pesquisar_monstro, todos_monstros)
                monstros_processados = [resultado for resultado in resultados if resultado is not None]
            return monstros_processados
        else:
            print(f'Erro ao obter a lista de monstros: {response.status_code}')
        return []
    finally:
        session.close()