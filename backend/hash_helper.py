import hashlib
import json

def generate_hash(emp_id, name, company, basic, net_pay, month, year):
    data = {
        "employeeId":  str(emp_id),
        "name":        name,
        "company":     company,
        "basicSalary": str(basic),
        "netPay":      str(net_pay),
        "month":       str(month),
        "year":        str(year)
    }
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()