from src.dao.pedido_dao import InserePedido
from src.model.models import Order, Order_details
from datetime import datetime

class PedidoController:
    @staticmethod
    def criarPedidoCompleto(customerid: str, employeeid: int, items: list, injection: bool = False):

        try:   
            print(f"Recebido - customerid: {customerid}, employeeid: {employeeid}, items: {items}")
            # Criar pedido principal
            orderid = int(datetime.now().timestamp())
            print(f"Novo orderid: {orderid}")
            pedido = Order(
                orderid=orderid,
                customerid=customerid,
                employeeid=employeeid,
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
                )
                if not InserePedido.inserir_item_pedido(item_obj):
                    InserePedido.removerPedido(orderid)  # Rollback
                    return False
                    
            return orderid
            
        except Exception as e:
            print(f"Erro no controller: {e}")
            return False