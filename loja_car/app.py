from flask import Flask, request, Response
from flask_cors import CORS
import mysql.connector
import config

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )


# ================================
# LISTAR CARROS (GET)
# ================================
@app.get("/listarCarros")
def listar_carros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, modelo, preco FROM carro")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    resposta = ""
    for r in rows:
        resposta += f'{{"id":{r[0]},"modelo":"{r[1]}","preco":{float(r[2])}}}'

    return Response(resposta, mimetype="text/plain")


# ================================
# ADICIONAR / ATUALIZAR CARRO (POST)
# ================================
@app.post("/saveCarro")
def salvar_carro():
    corpo = request.data.decode("utf-8").strip()

    try:
        modelo, preco = corpo.split(",")
        preco = float(preco)
    except:
        return Response("Formato inválido. Use: modelo,preco", status=400)

    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se modelo já existe
    cursor.execute("SELECT id FROM carro WHERE modelo = %s", (modelo,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute(
            "UPDATE carro SET preco = %s WHERE modelo = %s",
            (preco, modelo)
        )
        msg = f"Carro {modelo} atualizado"
    else:
        cursor.execute(
            "INSERT INTO carro (modelo, preco) VALUES (%s, %s)",
            (modelo, preco)
        )
        msg = f"Carro {modelo} adicionado"

    conn.commit()
    cursor.close()
    conn.close()

    return Response(msg, mimetype="text/plain")


# ================================
# DELETAR CARRO (POST)
# ================================
@app.post("/deleteCarro")
def deletar_carro():
    modelo = request.data.decode("utf-8").strip()
    if not modelo:
        return Response("Modelo não informado", status=400)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM carro WHERE modelo = %s", (modelo,))
    afetados = cursor.rowcount

    conn.commit()
    cursor.close()
    conn.close()

    if afetados == 0:
        return Response("Modelo não encontrado", status=404)

    return Response(f"Carro {modelo} deletado", mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
