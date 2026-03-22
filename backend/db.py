from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db     = client["paychain_db"]
payslips_collection = db["payslips"]

def save_payslip(data):
    payslips_collection.insert_one(data)

def get_payslip_by_empid(emp_id):
    results = list(payslips_collection.find(
        {"employeeId": emp_id},
        {"_id": 0}
    ))
    return results

def get_payslip_by_hash(hash_value):
    result = payslips_collection.find_one(
        {"payslipHash": hash_value},
        {"_id": 0}
    )
    return result