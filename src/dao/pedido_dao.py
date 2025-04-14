import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dao.database import connect

class InserePedido:
    @staticmethod
    def inserePedidoInjection(pedido):        
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO orders (orderid, customerid, employeeid, orderdate) "
                    f"VALUES ({pedido.orderid}, '{pedido.customerid}', {pedido.employeeid}, '{pedido.orderdate}')"
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
    def inserePedidoSeguro(pedido):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO orders (orderid, customerid, employeeid, orderdate) "
                    "VALUES (%s, %s, %s, %s)",
                    (pedido.orderid, pedido.customerid, pedido.employeeid, pedido.orderdate)
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
                    "INSERT INTO order_details (orderid, productid, quantity, unitprice) "
                    "VALUES (%s, %s, %s, %s)",
                    (item.orderid, item.productid, item.quantity, item.unitprice)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()