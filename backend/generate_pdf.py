from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

def generate_payslip_pdf(data):
    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(buffer, pagesize=A4,
                               rightMargin=40, leftMargin=40,
                               topMargin=40, bottomMargin=40)
    styles   = getSampleStyleSheet()
    elements = []
    navy     = colors.HexColor("#1a237e")
    white    = colors.white
    light    = colors.HexColor("#e8eaf6")
    green    = colors.HexColor("#2e7d32")

    gross   = data['basicSalary'] + data['hra'] + data['da'] + data['allowances']
    total_d = data['pf'] + data['esi'] + data['tds']
    net     = data['netPay']

    def rs(val):
        return f"Rs.{val}"

    # COMPANY HEADER
    header_data = [[
        Paragraph(f"<font size=16><b>{data['company'].upper()}</b></font>",
                  styles['Normal']),
        Paragraph("<font size=10 color='grey'>COMPANY LOGO</font>",
                  styles['Normal'])
    ]]
    header_table = Table(header_data, colWidths=[4*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN',         (1,0), (1,0), 'RIGHT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(header_table)

    # PAYSLIP TITLE
    title_data = [[
        Paragraph(
            f"<font size=12 color='white'><b>"
            f"Payslip for the Month of {data['month']}, {data['year']}"
            f"</b></font>",
            styles['Normal']
        )
    ]]
    title_table = Table(title_data, colWidths=[6.5*inch])
    title_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), navy),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(Spacer(1, 10))
    elements.append(title_table)
    elements.append(Spacer(1, 10))

    # EMPLOYEE INFO
    emp_info = [
        ["Employee Pay Summary", "", "", ""],
        ["Employee Name",  f": {data['name']}",         "", ""],
        ["Designation",    f": {data.get('designation','N/A')}", "", ""],
        ["Pay Period",     f": {data['month']}, {data['year']}",
         "Employee Net Pay", ""],
        ["Company",        f": {data['company']}",      "", rs(net)],
        ["PF A/C Number",  ": AA/AAA/0000000/000",
         "Paid Days: 30", "LOP Days: 0"],
    ]
    emp_table = Table(emp_info,
                      colWidths=[1.8*inch, 2*inch, 1.5*inch, 1.2*inch])
    emp_table.setStyle(TableStyle([
        ('SPAN',          (0,0), (3,0)),
        ('BACKGROUND',    (0,0), (3,0), light),
        ('FONTNAME',      (0,0), (3,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ALIGN',         (2,3), (3,5), 'CENTER'),
        ('FONTNAME',      (2,3), (3,4), 'Helvetica-Bold'),
        ('FONTSIZE',      (3,4), (3,4), 14),
        ('TEXTCOLOR',     (3,4), (3,4), green),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(emp_table)
    elements.append(Spacer(1, 10))

    # EARNINGS AND DEDUCTIONS
    sal_data = [
        ["EARNINGS",     "AMOUNT",    "YTD",
         "DEDUCTIONS",   "AMOUNT",    "YTD"],
        ["Basic Salary", rs(data['basicSalary']), rs(data['basicSalary']),
         "Provident Fund", rs(data['pf']),  rs(data['pf'])],
        ["HRA",          rs(data['hra']),  rs(data['hra']),
         "ESI",          rs(data['esi']),  rs(data['esi'])],
        ["DA",           rs(data['da']),   rs(data['da']),
         "TDS",          rs(data['tds']),  rs(data['tds'])],
        ["Allowances",   rs(data['allowances']), rs(data['allowances']),
         "", "", ""],
        ["Gross Earnings", rs(gross), "",
         "Total Deductions", rs(total_d), ""],
    ]
    sal_table = Table(sal_data,
                      colWidths=[1.5*inch, 1*inch, 1*inch,
                                 1.5*inch, 1*inch, 0.5*inch])
    sal_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (5,0), navy),
        ('TEXTCOLOR',     (0,0), (5,0), white),
        ('FONTNAME',      (0,0), (5,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,5), (5,5), 'Helvetica-Bold'),
        ('BACKGROUND',    (0,5), (5,5), light),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN',         (1,0), (-1,-1), 'RIGHT'),
    ]))
    elements.append(sal_table)
    elements.append(Spacer(1, 6))

    # NET PAY SUMMARY
    net_data = [
        ["NETPAY",          "", "", "", "", "AMOUNT"],
        ["Gross Earnings",  "", "", "", "", rs(gross)],
        ["Total Deductions","", "", "", "", rs(total_d)],
        ["Total Net Payable","","", "", "", rs(net)],
    ]
    net_table = Table(net_data,
                      colWidths=[2*inch, 0.8*inch, 0.8*inch,
                                 0.8*inch, 0.8*inch, 1.3*inch])
    net_table.setStyle(TableStyle([
        ('SPAN',          (0,0), (4,0)),
        ('BACKGROUND',    (0,0), (5,0), light),
        ('FONTNAME',      (0,0), (5,0), 'Helvetica-Bold'),
        ('FONTNAME',      (0,3), (5,3), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('ALIGN',         (5,0), (5,-1), 'RIGHT'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(net_table)
    elements.append(Spacer(1, 6))

    # FOOTER
    footer_data = [[
        Paragraph(
            f"<font size=9><b>Total Net Payable {rs(net)}</b><br/>"
            f"Total Net Payable = Gross Earnings - Total Deductions<br/>"
            f"Blockchain Hash: {data['payslipHash']}</font>",
            styles['Normal']
        )
    ]]
    footer_table = Table(footer_data, colWidths=[6.5*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND',    (0,0), (-1,-1), light),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    elements.append(footer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer