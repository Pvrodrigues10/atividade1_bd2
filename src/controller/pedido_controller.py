from src.dao.pedido_dao import InserePedido, ConsultaIds
from src.model.models import Order, Order_details
from datetime import datetime

class PedidoController:
    @staticmethod
    def criarPedidoCompleto(customer: str, employee: str, items: list, injection: bool = False):
        try:   
            print(f"Recebido - customerid: {customer}, employeeid: {employee}, items: {items}")
            
            # Consultar IDs de forma segura
            if injection:
                ids = ConsultaIds.consultar_ids_inseguro(employee, customer)
            else:
                ids = ConsultaIds.consultar_ids_seguro(employee, customer)
            
            if not ids['employee_ids'] or not ids['customer_ids']:
                print("Employee ou Customer não encontrado")
                return False
                
            employee_id = ids['employee_ids'][0]
            customer_id = ids['customer_ids'][0]
            
            # Criar pedido principal
            orderid = int(datetime.now().timestamp())
            print(f"Novo orderid: {orderid}")
            pedido = Order(
                orderid=orderid,
                customerid=customer_id,
                employeeid=employee_id,
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