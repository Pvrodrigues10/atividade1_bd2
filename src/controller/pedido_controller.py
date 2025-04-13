import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from dao.pedido_dao import InserePedido
from model.models import Order
# import time

class PedidoController:
    @staticmethod
    def criarPedidoInjection(customerid: str, employeeid: int, orderid: int):
        try:
            # Chama o DAO para inserir o pedido
            pedido = Order(orderid, customerid, employeeid)
            return InserePedido.inserePedidoInjection(pedido) 
            
        except ValueError as e:
            print(f"❌ Erro no Controller: {e}")
            return False
    
    def criarPedidoSeguro(customerid: str, employeeid: int, orderid: int):
        try:   
            # Chama o DAO para inserir o pedido
            pedido = Order(orderid, customerid, employeeid)
            return InserePedido.inserePedidoSeguro(pedido) 
            
        except ValueError as e:
            print(f"❌ Erro no Controller: {e}")
            return False



# def testar_injection():
#     print("\n=== TESTE DE SQL INJECTION SEGURO ===")
    
#     # Teste Time-Based (não altera dados)
#     payload = "LILAS'||(SELECT pg_sleep(3))||'"
    
#     print("⏳ Testando time-based injection...")
#     start = time.time()
#     PedidoController.criarPedidoInjection(payload, 3, 5)
#     elapsed = time.time() - start
    
#     if elapsed > 2.5:
#         print("⏱️ VULNERÁVEL! O banco dormiu por ~3s")
#     else:
#         print("🔒 SEGURO! Time-based injection bloqueada")

# if __name__ == "__main__":
    
#     # Teste de injeção
#     testar_injection()