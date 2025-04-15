from src.dao.pedido_dao import InserePedido, ConsultaIds
from src.dao.relatorios_dao import Consulta
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
        
        
    def consultaPedido(orderid: int):
        if not orderid:
            print("OrderID não fornecido")
            return None
        
        try:
            print(f"Consultando pedido com orderid: {orderid}")
            pedido_completo = Consulta.consultaPedidoCompleto(orderid)
            
            if not pedido_completo:
                print("Pedido não encontrado")
                return None
                
            return {
                "orderid": pedido_completo["orderid"],
                "orderdate": pedido_completo["orderdate"],
                "customerName": pedido_completo["customerName"],
                "employeeName": pedido_completo["employeeName"],
                "customerid": pedido_completo["customerid"],
                "employeeid": pedido_completo["employeeid"],
                "itens": pedido_completo["itens"]  
            }
            
        except Exception as e:
            print(f"Erro no Controller: {e}")
            return None
        
    def consultaRanking(startDate, endDate):
        if not startDate or not endDate:
            print("Datas não fornecidas")
            return None
        
        try:
            ranking = Consulta.rankingFuncionarios(startDate, endDate)
            if not ranking:
                print("Ranking não encontrado")
                return None
            print(ranking)
            return ranking
        
        except Exception as e:
            print(f"Erro no Controller: {e}")
            return None
        