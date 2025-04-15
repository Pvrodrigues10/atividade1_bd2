import sys
from pathlib import Path
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func, and_
from sqlalchemy.orm import aliased
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))
from dao.databaseORM import connect  # Agora usando a sessão do SQLAlchemy

# Configuração do ORM
Base = automap_base()
session = connect()  # Obtém a sessão do SQLAlchemy
engine = session.get_bind()
Base.prepare(engine, schema='northwind', reflect=True)

# Mapeamento das classes
Order = Base.classes.orders
Customer = Base.classes.customers
Employee = Base.classes.employees
OrderDetail = Base.classes.order_details
Product = Base.classes.products

class Consulta:
    @staticmethod
    def consultaPedido(orderid):
        try:
            pedido = session.query(Order).get(orderid)
            if pedido:
                return (pedido.orderid, pedido.orderdate, 
                        pedido.customerid, pedido.employeeid)
            return None
        except Exception as e:
            print(f"Erro ao consultar pedido: {e}")
            session.rollback()
            return None

    @staticmethod
    def consultaCustomerName(customerid):
        try:
            customer = session.query(Customer).get(customerid)
            return customer.companyname if customer else None
        except Exception as e:
            print(f"Erro ao consultar cliente: {e}")
            session.rollback()
            return None

    @staticmethod
    def consultaPedidoCompleto(orderid):
        try:
            pedido = session.query(Order).get(orderid)
            if not pedido:
                return None

            # Carrega os relacionamentos usando a sessão atual
            customer = session.query(Customer).get(pedido.customerid)
            employee = session.query(Employee).get(pedido.employeeid)

            # Consulta os itens com join
            itens = session.query(OrderDetail, Product)\
                .join(Product, OrderDetail.productid == Product.productid)\
                .filter(OrderDetail.orderid == orderid)\
                .all()

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
            session.rollback()
            return None

    @staticmethod
    def rankingFuncionarios(startDate, endDate):
        try:
            # Converte strings para objetos date se necessário
            if isinstance(startDate, str):
                startDate = datetime.strptime(startDate, '%Y-%m-%d').date()
            if isinstance(endDate, str):
                endDate = datetime.strptime(endDate, '%Y-%m-%d').date()

            # Cria alias para evitar conflitos
            od = aliased(OrderDetail)
            
            resultados = session.query(
                Employee.employeeid,
                func.concat(Employee.firstname, ' ', Employee.lastname).label('employee_name'),
                func.count(Order.orderid).label('total_pedidos'),
                func.sum(od.quantity * od.unitprice).label('total_vendido')
            ).join(
                Order, Employee.employeeid == Order.employeeid
            ).join(
                od, Order.orderid == od.orderid
            ).filter(
                and_(
                    Order.orderdate >= startDate,
                    Order.orderdate <= endDate
                )
            ).group_by(
                Employee.employeeid,
                'employee_name'
            ).order_by(
                func.sum(od.quantity * od.unitprice).desc()
            ).all()

            ranking = []
            for result in resultados:
                ranking.append({
                    "employeeid": result.employeeid,
                    "employee_name": result.employee_name,
                    "total_pedidos": result.total_pedidos,
                    "total_vendido": float(result.total_vendido) if result.total_vendido else 0.0
                })
                
            return ranking
            
        except Exception as e:
            print(f"Erro ao consultar ranking de funcionários: {e}")
            session.rollback()
            return None