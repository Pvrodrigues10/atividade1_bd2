import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Importações do projeto
from src.controller.pedido_controller import PedidoController

# Configuração de paths
TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "src" / "view" / "templates"

# Inicialização do Flask
app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
CORS(app)

# Rotas principais
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/novo_pedido")
def novo_pedido():
    return render_template("novo_pedido.html")

@app.route("/consulta_pedido")
def consulta_pedido():
    return render_template("consulta_pedido.html")

@app.route("/ranking")
def ranking():
    return render_template("ranking.html")

# API Endpoints
@app.route("/api/pedidos", methods=["POST"])
def cadastrar_pedido():
    try:
        dados = request.get_json()
        customer = dados.get("customer")
        employee = dados.get("employee")
        items = dados.get("items")

        # Verifica se o modo inseguro de injeção está ativado
        injection = request.headers.get("X-Injection-Mode", "false").lower() == "true"

        # Processa o pedido
        orderid = PedidoController.criarPedidoCompleto(
            customer, employee, items, injection
        )

        if orderid:
            return jsonify({"success": True, "orderid": orderid})
        return jsonify({"success": False, "detail": "Erro ao criar pedido"}), 400

    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500
    


@app.route("/api/consulta", methods=["GET"])
def api_consulta_pedido():
    try:
        orderid = request.args.get("orderid", type=int)
        if not orderid:
            return jsonify({
                "success": False,
                "detail": "OrderID é obrigatório"
            }), 400

        infosPedidos = PedidoController.consultaPedido(orderid)
        
        if infosPedidos:
            return jsonify({
                "success": True,
                "pedido": infosPedidos
            })
        return jsonify({
            "success": False,
            "detail": "Pedido não encontrado"
        }), 404
    
    except ValueError:
        return jsonify({
            "success": False,
            "detail": "OrderID deve ser um número válido"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "detail": f"Erro interno: {str(e)}"
        }), 500
        
@app.route("/api/ranking", methods=["GET"])
def api_ranking():
    try:
        startDate = request.args.get("startDate")
        endDate = request.args.get("endDate")
        print(f"StartDate: {startDate}, EndDate: {endDate}")
        ranking = PedidoController.consultaRanking(startDate, endDate)
        return jsonify({"success": True, "ranking": ranking})
    except Exception as e:
        return jsonify({"success": False, "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)