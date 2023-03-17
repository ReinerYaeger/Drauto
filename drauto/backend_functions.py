from datetime import datetime
import random
import string
from django.db import connection
from django.shortcuts import render, redirect

from drauto.models import Employee, EmergencyContact


def generate_cl_string(prefix):
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return prefix + random_chars


def findASalesPerson(emp_id=None):
    if emp_id == None:
        with connection.cursor() as cursor:
            cursor.execute("SELECT TOP 1 emp_Id FROM Salesman ORDER BY NEWID()")
            connection.commit()
            return cursor.fetchone()[0]

    if emp_id is not None:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM Salesman WHERE emp_id = '{emp_id}'")
            connection.commit()
            return cursor.fetchone()[0]


def findClient(client_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT client_id FROM Client WHERE client_name = '{client_name}'")
        connection.commit()
        return cursor.fetchone()[0]


def getPrice(chassis_number):
    # cursor.execute("SELECT DrautoshopAddb.dbo.GET_VEHICLES_SELL_PRICE() WHERE chassis_number = '{chassis_number}'")
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT Selling_Price FROM DrautoshopAddb.dbo.GET_VEHICLE_SELL_PRICE() WHERE chassis_number = '{chassis_number}'")
        data = cursor.fetchall()

        return data[0][0]


def getDiscountPrice(chassis_number):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DrautoshopAddb.dbo.GET_DISCOUNT('{chassis_number}')")
        data = cursor.fetchall()

        return data[0][0]


def update_employee(requests, emp_id, emp_emg_contact):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO DrautoshopAddb.dbo.Emergency_Contact(emergency_contact_number, emp_Id) VALUES('{emp_emg_contact}', '{emp_id}');""")
        connection.commit()
    return redirect('/')

def update_mechanic(requests,emp_id,salary,expertise):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM DrautoshopAddb.dbo.Mechanic WHERE emp_Id='{emp_id}'")
        record = cursor.fetchone()
        cursor.execute(f"SELECT * FROM DrautoshopAddb.dbo.Employee WHERE emp_Id='{emp_id}'")
        record2 = cursor.fetchone()

        if record:
            # Record exists, so update it
            cursor.execute(
                f"UPDATE DrautoshopAddb.dbo.Mechanic SET salary={salary}, expertise='{expertise}' WHERE emp_Id='{emp_id}'; ")
            connection.commit()
        elif record2:
            # Record doesn't exist, so insert it
            cursor.execute(
                f"INSERT INTO DrautoshopAddb.dbo.Mechanic (emp_Id, salary, expertise) VALUES ('{emp_id}', {salary}, '{expertise}');")
            connection.commit()
    return redirect('/')
