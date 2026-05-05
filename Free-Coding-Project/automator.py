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





def dupont(bs,in_s):
    for i in bs.keys():
      if "total assets" in i.lower():
         total_assets= int(bs[i][0])
         continue
      if "total shareholders' equity" in i.lower():
         total_equity = int(bs[i][0])
         continue
    for a in in_s.keys():
      if "sales" == a.lower() or "revenue" == a.lower():
         sales = int(in_s[a][0])
      if "net income" in a.lower():
         net_income = int(in_s[a][0])
         break
    
    b = f"Basic Ratios:\n\nNet Margin: {net_income/sales:.2f}\n\nTotal Asset Turnover: {sales/total_assets:.2f}\n\nLeverage: {total_assets/total_equity:.2f}"
    c= f"Dupont Ratios Combined:\n\nReturn On Equity: {net_income/total_equity:.2f}\n\nReturn On Assets: {net_income/total_assets:.2f}"

    print (f"{b}\n\n{c}\n")
    return



def efficiency(bs,in_s):
    for i in bs.keys():
      if "total assets" in i.lower():
         total_assets= int(bs[i][0])
         continue
    for i in bs.keys():
      if "fixed assets" in i.lower() or "ppe"in i.lower() or "property"in i.lower():
         fixed_assets= int(bs[i][0])
         continue
    for a in in_s.keys():
      if "sales" == a.lower() or "revenue" == a.lower():
         sales = int(in_s[a][0])
         continue
      if "operating income" in a.lower():
         op_income = int(in_s[a][0])
         continue
    b = f"\nEfficiency Ratios:\n\nTotal Asset Turnover: {sales/total_assets:.2f}\n\nFixed Asset Turnover: {sales/fixed_assets:.2f}\n\nOperating Income Return(OIROI): {op_income/total_assets:.2f}\n"
    print(b)


def financing(bs,in_s):
    for a in in_s.keys():
        if "operating income" in a.lower():
          op_income = int(in_s[a][0])
          continue
        if "total other income" in a.lower():
          other_income= int(in_s[a][0])
          continue
        else:
           other_income = 0
        if "interest expense" in a.lower():
           interest_expense = int(in_s[a][0])

    ebit= op_income+other_income



    
    for i in bs.keys():
        if "total assets" in i.lower():
          total_assets= int(bs[i][0])
          continue
        if "short-term debt"in i.lower():
          s_debt = int(bs[i][0])
          continue
        if "long-term debt" in i.lower():
           l_debt = int(bs[i][0])
           continue 
           
        
       
    b = f"\nFinancing Ratios:\n\nDebt Ratio: {(s_debt+l_debt)/total_assets:.2f}\n\nTIE: {ebit/abs(interest_expense):.2f}\n"
    print(b)

def free_cash_flows(bs,in_s,cf):
    other_income = 0
    for a in in_s.keys():
        if "operating income" in a.lower():
          op_income = int(in_s[a][0])
          continue
        if "total other income" in a.lower():
          other_income= int(in_s[a][0])
          continue
        if "tax expense" in a.lower():
           tax_expense= int(in_s[a][0])
           continue
        if "net income" in a.lower():
           net_income = int(in_s[a][0])
           break
    
    for i in bs.keys():


        if "fixed assets" in i.lower() or "ppe" in i.lower() or "property"in i.lower():
         fixed_assets2= int(bs[i][0])
         fixed_assets1 = int(bs[i][1])
         continue
        if "total current assets" in i.lower():
           c_asst2= int(bs[i][0])
           c_asst1= int(bs[i][1])
           continue
        if "total current liabilities" in i.lower():
           c_liab2= int(bs[i][0])
           c_liab1= int(bs[i][1])
           continue

        if "long-term debt" in i.lower():
           l_debt2= int(bs[i][0])
           l_debt1= int(bs[i][1])
           continue
    for c in cf.keys():
       if "depreciation and amortization" in c.lower():
          depreciation = int(cf[c][0])
          break
           
        
    
           
    
    capex = fixed_assets2-fixed_assets1 + depreciation
    change_net_working_cap= (c_asst2-c_liab2)-(c_asst1-c_liab1)
    ebit= op_income+other_income
    change_long_term_debt= l_debt2-l_debt1
    print(f"\nFree Cash Flow to the Firm: ${ebit-tax_expense+depreciation-change_net_working_cap-capex:,}\n\nFree Cash Flow to Equity: ${net_income+depreciation-capex-change_net_working_cap+change_long_term_debt:,}\n")
   
   
    
def liquidity(bs):
    for i in bs.keys():
      if "total current assets" in i.lower():
         current_assets= int(bs[i][0])
         continue
      if "total current liabilities" in i.lower():
         current_liabilities = int(bs[i][0])
         continue
      if "inventories" in i.lower():
         inventory= int(bs[i][0])
         continue
    
    print(f"\nCurrent Ratio: {current_assets/current_liabilities:.2f}\n\nQuick Ratio: {(current_assets-inventory)/current_liabilities:.2f}\n")


def profitability(bs,in_s):
  for a in bs.keys():
   
  
   if "total assets" in a.lower():
          total_assets= int(bs[a][0])
          continue

  for i in in_s.keys():
     if "sales" == i.lower() or "revenue" == i.lower():
         sales = int(in_s[i][0])
         continue
     if "gross profit" in i.lower():
          gross_profit= int(in_s[i][0])
          continue
     if "operating income" in i.lower():
          op_income = int(in_s[i][0])
          continue
     if "net income" == i.lower():
         net_income = int(in_s[i][0])
         continue
  
  print(f"\nTotal Asset Turnover: {sales/total_assets:.2f}\n\nReturn On Assets: {net_income/total_assets:.2f}\n\nGross Margin: {gross_profit/sales:.2f}\n\nOperating Margin: {op_income/sales:.2f}\n\nNet Margin: {net_income/sales:.2f}\n")
   

def return_on_investment(bs,in_s):
  for a in in_s:
    if "operating income" in a.lower():
          op_income = int(in_s[a][0])
          continue
    if "total other income" in a.lower():
          other_income= int(in_s[a][0])
          continue
    if "tax expense" in a.lower():
       tax_expense = int(in_s[a][0])
       continue
  for i in bs:
     if "total shareholders' equity" in i.lower():
         total_equity = int(bs[i][0])
         continue
     if "short-term debt"in i.lower():
          s_debt = int(bs[i][0])
          continue
     if "long-term debt" in i.lower():
           l_debt = int(bs[i][0])
           continue 
  ebit= op_income+other_income
  nopat= ebit-tax_expense
  costly_capital = s_debt+l_debt+total_equity
  print(f"\nROIC: {nopat/costly_capital:.2f}\n\nEconomic Profit(EVA): {economic_profit(nopat,costly_capital):.2f}")



def main():
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
   return



if __name__ == "__main__":
    main()




