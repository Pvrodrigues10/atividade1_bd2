from database import connect

class InserePedido:
    def inserePedidoInjection(pedido):        
        northwind = None
        try:
            northwind = connect()
            
            with northwind.cursor() as sessao:              
                sessao.execute(f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid})")
                
                # Recupera o ID do pedido inserido
                resultado = sessao.fetchone()
                print(f"Pedido inserido com sucesso! ID do pedido: {resultado[0]}")
                
                # Commit da transação
                northwind.commit()    
                            
        except Exception as e:
            print(f"❌ Erro durante a inserção: {e}")
            if northwind:
                sessao.close()
                northwind.rollback()
            return False
        
        finally:
            if northwind:
                sessao.close()
                northwind.close()
                return True
