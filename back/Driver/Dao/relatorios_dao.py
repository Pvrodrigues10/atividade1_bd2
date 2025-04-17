import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Dao.database import connect

class Consulta:
    def consultaPedido(orderid):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT orderid, orderdate, customerid, employeeid FROM northwind.orders WHERE orderid = %s",
                    (orderid,)
                )
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return None
        except Exception as e:
            print(f"Erro ao consultar pedido: {e}")
            return None
        finally:
            if conn: conn.close()
            
    def consultaCustomerName(customerid):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT contactname FROM northwind.customers WHERE customerid = %s",
                    (customerid,)
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
        except Exception as e:
            print(f"Erro ao consultar nome do cliente: {e}")
            return None
        finally:
            if conn: conn.close()
            
    def consultaPedidoCompleto(orderid):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                # Consulta principal
                cursor.execute("""
                    SELECT 
                        o.orderid,
                        o.orderdate,
                        c.contactname,
                        e.firstname,
                        e.lastname,
                        o.customerid,
                        o.employeeid
                    FROM northwind.orders o
                    JOIN northwind.customers c ON o.customerid = c.customerid
                    JOIN northwind.employees e ON o.employeeid = e.employeeid
                    WHERE o.orderid = %s
                """, (orderid,))
                
                pedido = cursor.fetchone()
                
                if not pedido:
                    return None
                
                # Consulta itens
                cursor.execute("""
                    SELECT 
                        od.productid,
                        p.productname,
                        od.quantity,
                        od.unitprice
                    FROM northwind.order_details od
                    JOIN northwind.products p ON od.productid = p.productid
                    WHERE od.orderid = %s
                """, (orderid,))
                
                itens = []
                for item in cursor.fetchall():
                    itens.append({
                        "productid": item[0],
                        "productname": item[1],
                        "quantity": item[2],
                        "unitprice": float(item[3]),
                        "subtotal": item[2] * float(item[3])
                    })
                
                return {
                    "orderid": pedido[0],
                    "orderdate": pedido[1].strftime("%Y-%m-%d %H:%M:%S") if pedido[1] else None,
                    "customerName": pedido[2],
                    "employeeName": f"{pedido[3]} {pedido[4]}",
                    "customerid": pedido[5],
                    "employeeid": pedido[6],
                    "itens": itens
                }
                
        except Exception as e:
            print(f"Erro ao consultar pedido completo: {e}")
            return None
        finally:
            if conn: conn.close()
            
    
    def rankingFuncionarios(startDate, endDate):
        conn = None
        try:
            conn = connect()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        e.employeeid,
                        CONCAT(e.firstname, ' ', e.lastname) AS employee_name,
                        COUNT(o.orderid) AS total_pedidos,
                        SUM(od.quantity * od.unitprice) AS total_vendido
                    FROM 
                        northwind.orders o
                    JOIN 
                        northwind.employees e ON o.employeeid = e.employeeid
                    JOIN 
                        northwind.order_details od ON o.orderid = od.orderid
                    WHERE 
                        o.orderdate BETWEEN %s AND %s
                    GROUP BY 
                        e.employeeid, employee_name
                    ORDER BY 
                        total_vendido DESC
                """, (startDate, endDate))
                
                raking = []
                for row in cursor.fetchall():
                    raking.append({
                        "employeeid": row[0],
                        "employee_name": row[1],
                        "total_pedidos": row[2],
                        "total_vendido": float(row[3])
                    })
                return raking
        except Exception as e:
            print(f"Erro ao consultar ranking de funcionários: {e}")
            return None
        finally:
            if conn: conn.close()