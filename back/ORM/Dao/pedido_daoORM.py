from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from Dao.databaseORM import connect
from Model.modelORM import Orders, OrderDetails, Employee, Customers

class InserePedido:
    @staticmethod
    def inserePedidoSeguro(pedido):
        session = connect()  # Obtém nova sessão
        try:
            new_order = Orders(
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
            new_item = OrderDetails(
                orderid=item.orderid,
                productid=item.productid,
                unitprice=item.unitprice,
                quantity=item.quantity
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
            
            customer_ids = session.query(Customers.customerid).filter(Customers.contactname == customer).all()
            
            return {
                'employee_ids': [row[0] for row in employee_ids],
                'customer_ids': [row[0] for row in customer_ids]
            }
        except Exception as e:
            print(f"Erro ao consultar IDs: {e}")
            return {'employee_ids': [], 'customer_ids': []}
        finally:
            session.close()