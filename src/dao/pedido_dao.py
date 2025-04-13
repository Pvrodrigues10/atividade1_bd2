import sys
sys.path.append('../')

from dao.database import connect

class InserePedido:
    def inserePedidoInjection(pedido):        
        northwind = None
        try:
            northwind = connect()
            
            with northwind.cursor() as sessao:              
                sessao.execute(f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid})")
                             
                # Commit da transação
                northwind.commit()
                print("✅ Pedido inserido com sucesso!")    
                            
        except Exception as e:
            print(f"❌ Erro durante a inserção: {e}")
            if northwind:
                northwind.rollback()
                sessao.close()
                northwind.close()
            return False
        
        finally:
            if northwind:
                sessao.close()
                northwind.close()
                return True
            
    
    def inserePedidoSeguro(pedido):
        northwind = None
        try:
            northwind = connect()
            
            with northwind.cursor() as sessao:              
                sessao.execute(f"INSERT INTO northwind.orders (orderid, customerid, employeeid) VALUES (%s, %s, %s)", (pedido.orderid, pedido.customerid, pedido.employeeid))
                
                # Commit da transação
                northwind.commit()
                print("✅ Pedido inserido com sucesso!")
                            
        except Exception as e:
            print(f"❌ Erro durante a inserção: {e}")
            if northwind:
                northwind.rollback()
                sessao.close()
                northwind.close()
            return False
        
        finally:
            if northwind:
                sessao.close()
                northwind.close()
                return True

