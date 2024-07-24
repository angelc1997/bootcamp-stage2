from fastapi import HTTPException
import mysql.connector
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.database import dbconfig


class MrtModel:
    def mrt_list():
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "SELECT m.mrt FROM attr_mrt JOIN mrts AS m ON mrt_id = m.id GROUP BY mrt_id ORDER BY COUNT(*) DESC"

            cursor.execute(sql_string)
            data = cursor.fetchall()

            return data

        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally: 
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()