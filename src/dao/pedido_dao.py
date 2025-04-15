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
                    "INSERT INTO northwind.order_details (orderid, productid, unitprice, quantity) "
                    "VALUES (%s, %s, %s, %s)",
                    (item.orderid, item.productid, item.unitprice, item.quantity)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn: conn.close()
            



class ConsultaIds:
    @staticmethod
    def consultar_ids_inseguro(employee, customer):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT orderid FROM northwind.employees WHERE firstname = {employee}')
                cursor.execute(f'SELECT orderid FROM northwind.customers WHERE contactname = {customer}')
                employeeid = [row[0] for row in cursor.fetchall()]
                return employeeid
        except Exception as e:
            print(f"Erro ao consultar IDs: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def consultar_ids_seguro(employee, customer):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                # Consulta segura para employee
                cursor.execute(
                    "SELECT employeeid FROM northwind.employees WHERE firstname = %s",
                    (employee,)
                )
                employee_ids = [row[0] for row in cursor.fetchall()]
                
                # Consulta segura para customer
                cursor.execute(
                    "SELECT customerid FROM northwind.customers WHERE contactname = %s",
                    (customer,)
                )
                customer_ids = [row[0] for row in cursor.fetchall()]
                
                return {
                    'employee_ids': employee_ids,
                    'customer_ids': customer_ids
                }
        except Exception as e:
            print(f"Erro ao consultar IDs: {e}")
            return {'employee_ids': [], 'customer_ids': []}
        finally:
            if conn: conn.close()