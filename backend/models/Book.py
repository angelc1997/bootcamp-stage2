from fastapi import HTTPException
import mysql.connector
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.database import dbconfig


class BookModel:
    def book_data(memberId):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()
            
            sql_string = "SELECT b.date, b.time, b.price, a.id AS attr_id, a.name AS attr_name, a.addr AS attr_addr, GROUP_CONCAT(i.url) AS urls FROM booking b LEFT JOIN attractions a ON b.attr_id = a.id LEFT JOIN images i ON a.id = i.attr_id WHERE b.member_id = %s GROUP BY b.id"
            
            cursor.execute(sql_string, (memberId,))
            all_data = cursor.fetchone()

            if not all_data:
                return None
            
            return all_data

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    def insert_booking(member_id, attr_id, date, time, price):

        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)

            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "SELECT * FROM booking WHERE member_id = %s"
            cursor.execute(sql_string, (member_id,))

            if cursor.fetchone():
                sql_string = "UPDATE booking SET attr_id = %s, date = %s, time = %s, price = %s WHERE member_id = %s"
                cursor.execute(sql_string, (attr_id, date, time, price, member_id))
            else:
                sql_string = "INSERT INTO booking (member_id, attr_id, date, time, price) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_string, (member_id, attr_id, date, time, price))

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

    def delete_booking(memberId):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "DELETE FROM booking WHERE member_id = %s"
            cursor.execute(sql_string, (memberId,))
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