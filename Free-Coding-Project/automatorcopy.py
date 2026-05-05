import csv
import sys

def read_in_financial_sheet(csv_financial_sheet_name):
    with open(csv_financial_sheet_name,"r") as file:
        fin_statement = csv.reader(file, delimiter=',')
        fin_statement=list(fin_statement)
    return fin_statement


def extract_dct(fin_statement):
    dct= {}
    for i in fin_statement:
        dct[i[0]]=i[1:]
    return dct

def correct_nums(dct):
    for i in dct.keys():
      for a in range(len(dct[i])):
         dct[i][a]= dct[i][a].replace("$", "").replace(",", "").strip()
         
    return dct


def validate(lst):
    if len(lst)==0:
        print("Error: No arguments given")
        return False
    if lst[0] == "-d" or lst[0]=="-p" or lst[0]== "-f" or lst[0]=="-e" or lst[0] == "-i":
      if len(lst)>=3:
         return True
      else:
         print("Error: No Income Statement, Balance Sheet")
         return False
    elif lst[0]=="-c":
       if len(lst)>=4:
         return True
       else:
         print("Error: No Income Statement, Balance Sheet, or Cash Flow Statement given")
       
    elif lst[0]=="-l":
      if len(lst)>1:
         return True
      else:
         print("No Balance Sheet given")
         return False
    else:
       print("Error: No category given")
      
    return



def economic_profit(nopat,costly_capital):
    wacc = (float(input("What is the Wacc percentage?: ")))/100
    return nopat-(wacc*costly_capital)





def dupont(bs, in_s):

    for i in bs.keys():
        name = i.lower()

        if "total assets" in name:
            total_assets = int(bs[i][0])
            continue

        elif any(k in name for k in ["total shareholders' equity", "total stockholders' equity", "total equity","total shareholders´ equity"]):
            total_equity = int(bs[i][0])
            continue

    for a in in_s.keys():
        name = a.lower()

        if any(k == name for k in ["revenue", "sales", "net sales", "total revenue"]):
            sales = int(in_s[a][0])
            continue

        elif "net income" in name:
            net_income = int(in_s[a][0])
            break

    b = f"""Basic Ratios:

   Net Margin: {net_income/sales:.2f}

   Total Asset Turnover: {sales/total_assets:.2f}

   Leverage: {total_assets/total_equity:.2f}"""

    c = f"""Dupont Ratios Combined:

   Return On Equity: {net_income/total_equity:.2f}

   Return On Assets: {net_income/total_assets:.2f}"""

    print(f"{b}\n\n{c}\n")
    return

def efficiency(bs, in_s):

    for i in bs.keys():
        name = i.lower()

        if "total assets" in name:
            total_assets = int(bs[i][0])
            continue

        elif any(k in name for k in ["ppe", "property", "plant", "equipment", "fixed assets"]):
            fixed_assets = int(bs[i][0])
            continue

    for a in in_s.keys():
        name = a.lower()

        if any(k == name for k in ["revenue", "sales", "net sales", "total revenue"]):
            sales = int(in_s[a][0])
            continue

        elif any(k in name for k in ["operating income", "income from operations", "operating profit"]):
            op_income = int(in_s[a][0])
            continue

    b = f"""
   Efficiency Ratios:

   Total Asset Turnover: {sales/total_assets:.2f}

   Fixed Asset Turnover: {sales/fixed_assets:.2f}

   Operating Income Return (OIROI): {op_income/total_assets:.2f}
    """
    print(b)

def financing(bs, in_s):

    
    other_income = 0
    interest_expense = 0

    for a in in_s.keys():
        name = a.lower()

        if any(k in name for k in ["operating income", "income from operations"]):
            op_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["total other income", "non-operating income"]):
            other_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["interest expense", "interest"]):
            interest_expense = int(in_s[a][0])
            continue

    ebit = op_income + other_income 

    for i in bs.keys():
        name = i.lower()

        if "total assets" in name:
            total_assets = int(bs[i][0])
            continue

        elif any(k in name for k in ["short-term debt", "current debt"]):
            s_debt = int(bs[i][0])
            continue

        elif any(k in name for k in ["long-term debt", "noncurrent debt"]):
            l_debt = int(bs[i][0])
            continue

    b = f"""
   Financing Ratios:

   Debt Ratio: {(s_debt + l_debt) / total_assets:.2f}

   TIE: {ebit / abs(interest_expense) if interest_expense != 0 else "Non computable, interest epense is Zero"}
   """
    print(b)



def free_cash_flows(bs, in_s, cf):

    other_income = 0
    tax_expense = 0
    depreciation = 0


    for a in in_s.keys():
        name = a.lower()

        if any(k in name for k in ["operating income", "income from operations"]):
            op_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["other income", "non-operating income"]):
            other_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["tax", "income tax"]):
            tax_expense = int(in_s[a][0])
            continue

        elif "net income" in name:
            net_income = int(in_s[a][0])
            break

    for i in bs.keys():
        name = i.lower()

        if any(k in name for k in ["property", "plant", "equipment", "ppe", "fixed assets"]):
            fixed_assets2 = int(bs[i][0])
            fixed_assets1 = int(bs[i][1])
            continue

        elif any(k in name for k in ["total current assets"]):
            c_asst2 = int(bs[i][0])
            c_asst1 = int(bs[i][1])
            continue

        elif any(k in name for k in ["total current liabilities"]):
            c_liab2 = int(bs[i][0])
            c_liab1 = int(bs[i][1])
            continue

        elif any(k in name for k in ["long-term debt", "noncurrent debt"]):
            l_debt2 = int(bs[i][0])
            l_debt1 = int(bs[i][1])
            continue

    for c in cf.keys():
        name = c.lower()

        if any(k in name for k in ["depreciation", "amortization"]):
            depreciation = int(cf[c][0])
            break

    capex = (fixed_assets2 - fixed_assets1) + depreciation
    change_net_working_cap = (c_asst2 - c_liab2) - (c_asst1 - c_liab1)
    change_long_term_debt = l_debt2 - l_debt1

    ebit = op_income + other_income

    fcff = ebit - tax_expense + depreciation - change_net_working_cap - capex

    fcfe = net_income + depreciation - capex - change_net_working_cap + change_long_term_debt

    print(f"""
    Free Cash Flow to the Firm: ${fcff:,}

    Free Cash Flow to Equity: ${fcfe:,}
    """)
    
def liquidity(bs):

   
    
    inventory = 0

    for i in bs.keys():
        name = i.lower()

        if any(k in name for k in ["total current assets"]):
            current_assets = int(bs[i][0])

        elif any(k in name for k in ["total current liabilities"]):
            current_liabilities = int(bs[i][0])

        elif any(k in name for k in ["inventories", "inventory"]):
            inventory = int(bs[i][0])

    print(f"""
    Current Ratio: {current_assets / current_liabilities:.2f}

    Quick Ratio: {(current_assets - inventory) / current_liabilities:.2f}
    """)

def profitability(bs, in_s):


    for a in bs.keys():
        name = a.lower()

        if any(k in name for k in ["total assets"]):
            total_assets = int(bs[a][0])

    for i in in_s.keys():
        name = i.lower()

        if any(k == name for k in ["revenue", "sales", "net sales", "total revenue"]):
            sales = int(in_s[i][0])

        elif any(k in name for k in ["gross profit", "gross margin"]):
            gross_profit = int(in_s[i][0])

        elif any(k in name for k in ["operating income", "income from operations"]):
            op_income = int(in_s[i][0])

        elif any(k == name for k in ["net income"]):
            net_income = int(in_s[i][0])

    print(f"""
    Total Asset Turnover: {sales / total_assets:.2f}

    Return On Assets: {net_income / total_assets:.2f}

    Gross Margin: {gross_profit / sales:.2f}

    Operating Margin: {op_income / sales:.2f}

    Net Margin: {net_income / sales:.2f}
    """)

def return_on_investment(bs, in_s):


    for a in in_s.keys():
        name = a.lower()

        if any(k in name for k in ["operating income", "income from operations"]):
            op_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["total other income", "non-operating income", "other income/(expense), net", "Other income, net"]):
            other_income = int(in_s[a][0])
            continue

        elif any(k in name for k in ["tax", "income tax"]):
            tax_expense = int(in_s[a][0])
            continue

    
    for i in bs.keys():
        name = i.lower()

        if any(k in name for k in ["shareholders' equity", "stockholders' equity", "total equity"]):
            total_equity = int(bs[i][0])
            continue

        elif any(k in name for k in ["short-term debt", "current debt"]):
            s_debt = int(bs[i][0])
            continue

        elif any(k in name for k in ["long-term debt", "noncurrent debt"]):
            l_debt = int(bs[i][0])
            continue

    ebit = op_income + other_income
    nopat = ebit - tax_expense

    costly_capital = s_debt + l_debt + total_equity

    print(f"""
    ROIC: {nopat / costly_capital:.2f}

    Economic Profit (EVA): {economic_profit(nopat, costly_capital):.2f}
    """)

def main():
   try:
       args = sys.argv[1:]
       if not validate(args):
         print("Error: Invalid arguments")
         return
       category= args[0]
       bs= args[1]
       in_s= args[2]
       cf = args[3]
       bs=read_in_financial_sheet(bs)
       bs = correct_nums(extract_dct(bs))
       in_s= read_in_financial_sheet(in_s)
       in_s= correct_nums(extract_dct(in_s))
       cf= read_in_financial_sheet(cf)
       cf= correct_nums(extract_dct(cf))
       if category == "-d":
         dupont(bs,in_s)
       if category == "-e":
         efficiency(bs,in_s)
       if category == "-f":
         financing(bs,in_s)
       if category == "-c":
         free_cash_flows(bs, in_s,cf)
       if category == "-l":
        liquidity(bs)
       if category == "-p":
         profitability(bs,in_s)
       if category == "-i":
        return_on_investment(bs,in_s)
   except UnboundLocalError:
       print("Error: Name of account not found, please change to standard names")
       
   return

   
   



if __name__ == "__main__":
    main()




