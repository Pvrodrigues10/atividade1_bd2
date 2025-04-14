class Order:
    def __init__(self, orderid=None, customerid=None, employeeid=None, orderdate=None):
        self.orderid = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.orderdate = orderdate
        
class Order_details:
    def __init__(self, orderid=None, productid=None, quantity=None, unitprice=None):
        self.orderid = orderid
        self.productid = productid
        self.quantity = quantity
        self.unitprice = unitprice