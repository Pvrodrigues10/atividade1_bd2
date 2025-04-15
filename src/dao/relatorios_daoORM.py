import sys
from pathlib import Path
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from dao.database import connect  

sys.path.append(str(Path(__file__).parent.parent))

# Configuração do ORM usando a conexão existente
conn = connect()
Base = automap_base()

# Reflete o schema usando a conexão do psycopg
Base.prepare(conn, schema='northwind', reflect=True)

# Mapeamento das classes
Order = Base.classes.orders
Customer = Base.classes.customers
Employee = Base.classes.employees
OrderDetail = Base.classes.order_details
Product = Base.classes.products

# Configuração da sessão
Session = sessionmaker(bind=conn)

class Consulta:
    @staticmethod
    def consultaPedido(orderid):
        session = Session()
        try:
            pedido = session.query(Order).get(orderid)
            return (pedido.orderid, pedido.orderdate, 
                    pedido.customerid, pedido.employeeid) if pedido else None
        except Exception as e:
            print(f"Erro ao consultar pedido: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def consultaCustomerName(customerid):
        session = Session()
        try:
            customer = session.query(Customer).get(customerid)
            return customer.companyname if customer else None
        except Exception as e:
            print(f"Erro ao consultar cliente: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def consultaPedidoCompleto(orderid):
        session = Session()
        try:
            pedido = session.query(Order).get(orderid)
            if not pedido:
                return None

            # Carrega os relacionamentos
            customer = session.query(Customer).get(pedido.customerid)
            employee = session.query(Employee).get(pedido.employeeid)

            # Consulta os itens
            itens = session.query(OrderDetail, Product).join(
                Product, OrderDetail.productid == Product.productid
            ).filter(OrderDetail.orderid == orderid).all()

            detalhes = []
            for item, produto in itens:
                detalhes.append({
                    "productid": item.productid,
                    "productname": produto.productname,
                    "quantity": item.quantity,
                    "unitprice": float(item.unitprice),
                    "subtotal": item.quantity * float(item.unitprice)
                })

            return {
                "orderid": pedido.orderid,
                "orderdate": pedido.orderdate.strftime("%Y-%m-%d %H:%M:%S"),
                "customerName": customer.companyname,
                "employeeName": f"{employee.firstname} {employee.lastname}",
                "customerid": pedido.customerid,
                "employeeid": pedido.employeeid,
                "itens": detalhes
            }
            
        except Exception as e:
            print(f"Erro ao consultar pedido completo: {e}")
            return None
        finally:
            session.close()