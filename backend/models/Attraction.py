from fastapi import HTTPException
import mysql.connector
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.database import dbconfig



class AttractionModel:
    def get_attr_list(page, keyword):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            page_size = 13
            offset = page * 12
            
            sql_string = "SELECT attractions.*, (SELECT CONCAT(GROUP_CONCAT(CONCAT(images.url))) FROM images WHERE images.attr_id = attractions.id) AS urls FROM attractions"   

            if keyword:
                sql_string += " WHERE mrt = %s OR name LIKE %s LIMIT %s OFFSET %s" 
                cursor.execute(sql_string, (keyword, f"%{keyword}%", page_size, offset))
            else:
                sql_string += " LIMIT %s OFFSET %s"
                cursor.execute(sql_string, (page_size, offset))

            all_data = cursor.fetchall()

            return all_data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally: 
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    
    def get_attr_detail(attractionId):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig) 
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()
           
            info_sql_string = "SELECT * FROM attractions WHERE id = %s"
            picture_sql_string = "SELECT url FROM images WHERE attr_id = %s"
           
            cursor.execute(info_sql_string, (attractionId,))
            info = cursor.fetchone()
           
            cursor.execute(picture_sql_string, (attractionId,))
            picture_data = [row[0] for row in cursor.fetchall()]
           
            if info is None:
                return None
            
            if info:
                data = list(info) + [picture_data]
                return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally: 
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

