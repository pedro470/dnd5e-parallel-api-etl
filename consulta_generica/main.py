import db
import consulta_paralela

conn = db.criar_conexao()
#resultado_monstros = consulta_paralela.consulta_paralela()
#if resultado_monstros:
#    db.inserir_varios_monstros(conn, resultado_monstros)
monstros_no_banco = db.buscar_todos_monstros(conn)
for monstro in monstros_no_banco:
    print(monstro)
db.fechar_conexao(conn)