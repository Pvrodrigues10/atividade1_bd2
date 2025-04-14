from src.dao.pedido_dao import InserePedido
from src.model.models import Order, Order_details
from datetime import datetime

class PedidoController:
    @staticmethod
    def criarPedidoCompleto(customerid: str, employeeid: int, orderdate: str, items: list, injection: bool = False):
        try:
            # Validações
            if len(customerid) != 5:
                raise ValueError("ID do cliente deve ter 5 caracteres")
            if not items:
                raise ValueError("Adicione pelo menos um item ao pedido")
            
            # Criar pedido principal
            orderid = int(datetime.now().timestamp())
            pedido = Order(
                orderid=orderid,
                customerid=customerid,
                employeeid=employeeid,
                orderdate=orderdate
            )
            
            # Inserir pedido
            if injection:
                success = InserePedido.inserePedidoInjection(pedido)
            else:
                success = InserePedido.inserePedidoSeguro(pedido)
            
            if not success:
                return False
                
            # Inserir itens
            for item in items:
                item_obj = Order_details(
                    orderid=orderid,
                    productid=item['productid'],
                    quantity=item['quantity'],
                    unitprice=item['unitprice']
                )
                if not InserePedido.inserir_item_pedido(item_obj):
                    InserePedido.removerPedido(orderid)  # Rollback
                    return False
                    
            return orderid
            
        except Exception as e:
            print(f"Erro no controller: {e}")
            return False