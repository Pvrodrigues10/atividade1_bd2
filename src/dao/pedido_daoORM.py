from datetime import datetime
import sys
from pathlib import Path
from sqlalchemy.ext.automap import automap_base

sys.path.append(str(Path(__file__).parent.parent))
from dao.databaseORM import connect
conn = connect()

# Configuração do ORM com reflexão automática
Base = automap_base()
engine = connect().get_bind()  # Obtém o engine da sessão
Base.prepare(engine, schema='northwind', reflect=True)

# Mapeamento das classes
Order = Base.classes.orders
OrderDetail = Base.classes.order_details
Employee = Base.classes.employees
Customer = Base.classes.customers

class InserePedido:
    @staticmethod
    def inserePedidoSeguro(pedido):
        session = connect()  # Obtém nova sessão
        try:
            new_order = Order(
                orderid=pedido.orderid,
                customerid=pedido.customerid,
                employeeid=pedido.employeeid,
                orderdate=datetime.now()
            )
            session.add(new_order)
            session.commit()
            return True
        except Exception as e:
            print(f"Erro durante a inserção: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def inserir_item_pedido(item):
        session = connect()
        try:
            new_item = OrderDetail(
                orderid=item.orderid,
                productid=item.productid
            )
            session.add(new_item)
            session.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir item: {e}")
            session.rollback()
            return False
        finally:
            session.close()

class ConsultaIds:
    @staticmethod
    def consultar_ids_seguro(employee, customer):
        session = connect()
        try:
            # Consulta usando ORM
            employee_ids = session.query(Employee.employeeid).filter(Employee.firstname == employee).all()
            
            customer_ids = session.query(Customer.customerid).filter(Customer.contactname == customer).all()
            
            return {
                'employee_ids': [row[0] for row in employee_ids],
                'customer_ids': [row[0] for row in customer_ids]
            }
        except Exception as e:
            print(f"Erro ao consultar IDs: {e}")
            return {'employee_ids': [], 'customer_ids': []}
        finally:
            session.close()