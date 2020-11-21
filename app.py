import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# change @app.route('/cars') to: @app.route('/api/cars')
@app.route('/api/cars', methods=['GET','POST','PATCH','DELETE'])
def cars():
    if request.method == 'GET':
        conn = None
        cursor = None
        cars = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM car")
            cars = cursor.fetchall()
            # return Response()
        except Exception as error:
            print("Something went wrong: ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(cars != None):
                 return Response(json.dumps(cars, default=str), mimetype="application/json", status=200)
            else:
                 return Response("Something went wrong!", mimetype="text/html", status=500)

    elif request.method == 'POST':
        conn = None
        cursor = None
        car_name = request.json.get("name")
        car_description = request.json.get("description")
        car_image = request.json.get("image")
        row = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO car(name, description, image) VALUES(?, ?, ?)", [car_name, car_description, car_image])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                 conn.rollback()
                 conn.close()
            if(rows == 1):
                return Response("Car Inserted!", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        car_name = request.json.get("name")
        car_description = request.json.get("description")
        car_image = request.json.get("image")
        car_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if car_name != "" and car_name != None:
                cursor.execute("UPDATE car SET name=? WHERE id=?", [car_name, car_id])
            if car_description != "" and car_description != None:
                cursor.execute("UPDATE car SET description=? WHERE id=?", [car_description, car_id])
            if car_image != "" and car_image != None:
                cursor.execute("UPDATE car SET image=? WHERE id=?", [car_image, car_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY!)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Updated successfully", mimetype="text/html", status=204)
            else: 
                return Response("Update failed", mimetype="text/html", status=500)
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        car_id = request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM car WHERE id=?", [car_id,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY!)")
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None:
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Deleted successfully", mimetype="text/html", status=204)
            else: 
                return Response("Delete failed", mimetype="text/html", status=500)