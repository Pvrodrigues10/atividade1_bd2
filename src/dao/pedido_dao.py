import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dao.database import connect

class InserePedido:
    def inserePedidoInjection(pedido):        
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO northwind.orders (orderid, customerid, employeeid) "
                    f"VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid})"
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro durante a inserção: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()
    
    def inserePedidoSeguro(pedido):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO northwind.orders (orderid, customerid, employeeid) "
                    "VALUES (%s, %s, %s)",
                    (pedido.orderid, pedido.customerid, pedido.employeeid)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro durante a inserção: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def inserir_item_pedido(item):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO northwind.order_details (orderid, productid) "
                    "VALUES (%s, %s)",
                    (item.orderid, item.productid)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()