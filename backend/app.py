from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from web3 import Web3
from hash_helper import generate_hash
from db import save_payslip, get_payslip_by_empid, get_payslip_by_hash
from generate_pdf import generate_payslip_pdf
import json

app = Flask(__name__)
CORS(app)

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load contract
with open("../build/contracts/PayslipContract.json") as f:
    contract_json = json.load(f)

abi              = contract_json["abi"]
CONTRACT_ADDRESS = "0x39b8223b99690c6Dc679D77C6c90650C90d6d1D3"
contract         = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
hr_account       = w3.eth.accounts[0]


# PAGE ROUTES
@app.route("/")
@app.route("/hr")
def hr_page():
    return render_template("hr.html")

@app.route("/employee")
def employee_page():
    return render_template("employee.html")

@app.route("/verify")
def verify_page():
    return render_template("verify.html")


# API 1 — Generate Payslip
@app.route("/generate", methods=["POST"])
def generate():
    data        = request.json
    emp_id      = int(data["employeeId"])
    name        = data["name"]
    company     = data["company"]
    designation = data.get("designation", "N/A")
    basic       = int(data["basicSalary"])
    hra         = int(data["hra"])
    da          = int(data["da"])
    allow       = int(data["allowances"])
    pf          = int(data["pf"])
    esi         = int(data["esi"])
    tds         = int(data["tds"])
    month       = int(data["month"])
    year        = int(data["year"])

    net_pay  = (basic + hra + da + allow) - (pf + esi + tds)
    pay_hash = generate_hash(
        emp_id, name, company, basic, net_pay, month, year
    )

    tx = contract.functions.generatePayslip(
        emp_id, name, company, basic, net_pay, month, year, pay_hash
    ).transact({"from": hr_account})

    save_payslip({
        "employeeId":   emp_id,
        "name":         name,
        "company":      company,
        "designation":  designation,
        "basicSalary":  basic,
        "hra":          hra,
        "da":           da,
        "allowances":   allow,
        "pf":           pf,
        "esi":          esi,
        "tds":          tds,
        "netPay":       net_pay,
        "month":        month,
        "year":         year,
        "payslipHash":  pay_hash,
        "txHash":       tx.hex()
    })

    return jsonify({
        "success":     True,
        "txHash":      tx.hex(),
        "payslipHash": pay_hash,
        "netPay":      net_pay
    })


# API 2 — Get Payslip by Employee ID
@app.route("/payslip/<int:emp_id>", methods=["GET"])
def get_payslip(emp_id):
    results = get_payslip_by_empid(emp_id)
    if results:
        return jsonify({"success": True, "payslips": results})
    return jsonify({"success": False, "message": "No payslips found"})


# API 3 — Verify Payslip
@app.route("/verify-check", methods=["POST"])
def verify_check():
    data       = request.json
    emp_id     = int(data["employeeId"])
    hash_value = data["payslipHash"]

    payslip = get_payslip_by_hash(hash_value)

    if payslip:
        return jsonify({
            "success": True,
            "genuine": True,
            "payslip": payslip
        })

    try:
        is_genuine = contract.functions.verifyPayslip(
            emp_id, hash_value
        ).call()
        if is_genuine:
            return jsonify({
                "success": True,
                "genuine": True,
                "payslip": None
            })
    except:
        pass

    return jsonify({
        "success": True,
        "genuine": False,
        "message": "FAKE — This payslip has been tampered!"
    })


# API 4 — Download Payslip PDF
@app.route("/download/<int:emp_id>/<string:hash_value>", methods=["GET"])
def download(emp_id, hash_value):
    payslip = get_payslip_by_hash(hash_value)
    if not payslip:
        return jsonify({"error": "Payslip not found"}), 404
    pdf = generate_payslip_pdf(payslip)
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"payslip_{emp_id}_{payslip['month']}_{payslip['year']}.pdf"
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000)