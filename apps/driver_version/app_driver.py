import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Adiciona o diretório raiz do projeto (onde está a pasta src) ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Agora podemos importar do src normalmente
from src.controller.pedido_controller import PedidoController

# Caminho absoluto da pasta de templates
TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "src" / "view" / "templates"

# Inicializa o app Flask com o template_folder correto
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
CORS(app)  # Libera o uso de fetch() e AJAX no navegador

# Rota principal - carrega o formulário HTML
@app.route("/")
def form():
    return render_template("novo_pedido.html")


# Rota da API que o formulário envia os dados
@app.route("/api/pedidos", methods=["POST"])
def cadastrar_pedido():
    try:
        dados = request.get_json()
        print(dados)
        customer = dados.get("customer")
        employee = dados.get("employee")
        items = dados.get("items")

        # Verifica se o cabeçalho "X-Injection-Mode" está ativado
        injection = request.headers.get("X-Injection-Mode", "false").lower() == "true"

        # Chama o controller
        orderid = PedidoController.criarPedidoCompleto(
            customer, employee, items, injection
        )

        if orderid:
            return jsonify({"success": True, "orderid": orderid})
        else:
            return jsonify({"success": False, "detail": "Erro ao criar pedido"}), 400

    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500


# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
