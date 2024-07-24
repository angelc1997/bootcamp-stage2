from fastapi import HTTPException
import mysql.connector
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.database import dbconfig
from src.token import tokenconfig


SECRET_KEY = tokenconfig["SECRET_KEY"]
ALGORITHM = tokenconfig["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]


class OrderModel():
    def insert_order(buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img):

        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "INSERT INTO orders(buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(sql_string, (buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img))
            
            cnx.commit()
            
            order_id = cursor.lastrowid
            return order_id

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
    def insert_paidlist(order_id, paid_status, order_number):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "INSERT INTO paidlist(order_id, paid_status, order_number) VALUES (%s, %s, %s)"

            cursor.execute(sql_string, (order_id, paid_status, order_number))
            
            cnx.commit()
            
            return True

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        
    def get_paid_order(orderNumber):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()
            
            sql_string = "SELECT o.*, p.* FROM orders o LEFT JOIN paidlist p ON o.id = p.order_id WHERE p.order_number = %s;"

            cursor.execute(sql_string, (orderNumber,))

            data = cursor.fetchone()

            return data

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()