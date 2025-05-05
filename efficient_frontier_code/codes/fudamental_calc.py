import pandas as pd
class fundamentals():
    def __init__(self):
        self.info=dict()
        self.results=''
        self.main()
        
    def eps(self):
        print("Calculating EPS, P/E, PEG:")
        while True:
            try:
                shares=float(input("Enter shares outstanding: "))
                net_profit=float(input("Enter net profit: "))
                price=float(input("Enter the market price of each share: "))
                growth=float(input("Enter the future growth prospect as a percentage: "))
                self.info['EPS']=net_profit/shares
                self.info['P/E']=price/self.info['EPS']
                self.info['PEG']=self.info['P/E']/growth
                print("Data added - EPS, P/E, PEG")
                print("-----------------------------------------------------------------------------")
                return
            except:
                print("Please enter appropriate input!")
        return 

    @staticmethod
    def pb():
        print("Calculating P/B:")
        while True:
            try:
                shares=float(input('Enter total shares outstanding: '))
                tang_assets=float(input("Enter the total tangible assets: "))
                liab=float(input('Enter the total liabilities: '))
                print("Data added - P/B")
                print("-----------------------------------------------------------------------------")
                return 'P/B',(tang_assets-liab)/shares
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def gpm():
        print("Calculating GPM:")
        while True:
            try:
                gross=float(input('Enter the gross profit(profit after deducting COGS only): '))
                sales=float(input("Enter the net sales/revenue earned: "))
                print("Data added - GPM")
                print("-----------------------------------------------------------------------------")
                return 'GPM',gross/sales
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def opm():
        print("Calculating OPM:")
        while True:
            try:
                op=float(input("Enter operational profit (EBIT/EBITDA): "))
                sales=float(input("Enter the net sales/revenue: "))
                print("Data added - OPM")
                print("-----------------------------------------------------------------------------")
                return 'OPM',op/sales
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def itr():
        print("Calculating ITR:")
        while True:
            try:
                cogs=float(input("Enter the cost of goods sold: "))
                inventory=float(input("Enter the average inventory at a time: "))
                print("Data added - ITR")
                print("-----------------------------------------------------------------------------")
                return 'ITR',cogs/inventory
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def cr():
        print("Calculating CR:")
        while True:
            try:
                c_ass=float(input("Enter the total current assets: "))
                c_liab=float(input("Enter the current Liabilities: "))
                print("Data added - CR")
                print("-----------------------------------------------------------------------------")
                return 'CR',c_ass/c_liab
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def qr():
        print("Calculating QR:")
        while True:
            try:
                c_ass=float(input("Enter the total current assets: "))
                c_liab=float(input("Enter the current Liabilities: "))
                inventory=float(input("Enter the total inventory: "))
                print("Data added - QR")
                print("-----------------------------------------------------------------------------")
                return 'QR',(c_ass-inventory)/c_liab
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def icr():
        print("Calculating ICR:")
        while True:
            try:
                interest=float(input("Enter the interest to be paid: "))
                ebit=float(input("Enter EBIT: "))
                print("Data added - ICR")
                print("-----------------------------------------------------------------------------")
                return 'ICR',interest/ebit
            except:
                print("Please enter appropriate input!")
        return
    
    @staticmethod
    def de():
        print("Calculating D/E:")
        while True:
            try:
                debt=float(input('Enter the total debt: '))
                eq=float(input('Enter the total equity: '))
                print("Data added - D/E")
                print("-----------------------------------------------------------------------------")
                return 'D/E',debt/eq
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def da():
        print("Calculating D/A:")
        while True:
            try:
                debt=float(input("Enter the total debt: "))
                assets=float(input("Enter the total assets: "))
                print("Data added - D/A")
                print("-----------------------------------------------------------------------------")
                return 'D/A',debt/assets
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def roceq():
        print("Calculating RoCEq:")
        while True:
            try:
                amt=float(input("Enter the amount after deduction of preferred equity from net profit: "))
                ce=float(input("Enter the common equity amount: "))
                print("Data added - RoCEq")
                print("-----------------------------------------------------------------------------")
                return 'RoCEq',amt/ce
            except:
                print("Please enter appropriate input!")
        return

    @staticmethod
    def roce():
        print("Calculating RoCE:")
        while True:
            try:
                cap=float(input("Enter the total cap employed: "))
                op=float(input("Enter the operational profit (EBIT/EBITDA): "))
                print("Data added - RoCE")
                print("-----------------------------------------------------------------------------")
                return 'RoCE',op/cap
            except:
                print("Please enter appropriate input!")
        return
    
    @staticmethod
    def p_growth():
        print("Calculating Profit Growth:")
        while True:
            try:
                cp=float(input("Enter current year net profit: "))
                pp=float(input("Enter previous year net profit: "))
                print("Data added - Profit Growth")
                print("-----------------------------------------------------------------------------")
                return 'Net Profit Growth',(cp-pp)*100/abs(pp)
            except:
                print("Please enter appropriate input!")
        return

    def calc_all(self):
        for k in self.menu.keys():
            if(k==1):
                self.menu[k](self)
                continue
            if(k==14 or k==15):
                continue
            name,value=self.menu[k]()
            self.info[name]=value
        print("All calculations done, check the results")
        return               
        
    def result(self):
        self.result=pd.Series(self.info,dtype='float')
        n=int(input('Do you want the pointers? Press 1 if yes: '))
        print('''-----------------------------------------------------------------------------''')
        print("Results:\n")
        print(self.result)
        if n:
            print('''-----------------------------------------------------------------------------
    Some points to remember for comparing results:
    1. Always look at financials at least over a period of 3-5 years
    2. For asset heavy industries, compare EBITDA. For others, use EBIT.
    3. Make sure that ICR > 3 (Ideal)
    4. Make sure that DR < 0.5 (Ideal)
    5. Make sure that D/E < 1
    6.Make sure that CR > 1.33 (Ideal)
    7. Make sure that QR > 1 (ideal)
    8. When checking RoCEq make sure to also check out the debt parameters, because the ration may be riged by minimizing equity and having more debts.
    9. More thatn RoCEq check the RoCE so as to make sure that the returns on the cap employed are good, which in turn will mean the co. is efficient.
    10. Avoid stocks with P/B ratios < 1
    11. After finding out the P/E Ratio, always check the PEG ratio to justify the current mkt price of the share.
    12. For asset heavy industries, compare P/B (because they have more assets) to get a better picture of the justified price for the company.
    13. For asset light industries like software, P/B ratio is very high and thus aint so useful because they hardly have any heavy assets like machinery, plants etc.
    Thus compare the P/E ratio followed by the PEG ratio in these cases.
    14. If GPM over the years is almost similar but the OPM increases well enough, it means that the company is being able to manage its operating costs quite well.
    [Note: Operating profit is the profit left after the marketing, admin, ad etc costs (known as operating costs) have been deucted. Thus if OPM increases, then it
    means that the company is able to mitigate its operating costs over the years, thus boosting profits.]

    Preferred priority of checking the ratios:
    1. Returns  2. Profit Grwoth  3. Debt   4. Price(P/E)   5. PEG (Check if the OPM is increasing over the years/yoy profits)''')
        return
    
    menu={
        1:eps,
        2:pb.__func__,
        3:gpm.__func__,
        4:opm.__func__,
        5:itr.__func__,
        6:cr.__func__,
        7:qr.__func__,
        8:icr.__func__,
        9:de.__func__,
        10:da.__func__,
        11:roceq.__func__,
        12:roce.__func__,
        13:p_growth.__func__,
        14:calc_all,
        15:result
    }
    ''' eps.__func__ --> Creating a static method object. The __func__ is used to actually use the underlying function. If it wasn't used we wouldnt have been able to call the function, because
            it would otherwise have been a static method object only, not bound to anything (like, classname.staticobj --> this works), and a static method needs to be bound to the class to enable it
            to be called. Thus using __func__we actually can use the underlying raw function without having to bind it with the class.
        '''
    '''Static methods have a limited use case because, like class methods or any other methods within a class, they cannot access the properties of the class itself.
    However, when you need a utility function that doesn't access any properties of a class but makes sense that it belongs to the class, we use static functions.'''
     
    def main(self):
        while True:
            print('''-----------------------------------------------------------------------------
(Note: Performing an action a second time will overwrite its previously recorded result)
Available functions:
1. EPS, P/E and PEG
2. P/B
3. Gross Profit Margin
4. Operating Profit Margin
5. Inventory Turnover ratio
6. Current Ratio
7. Quick Ratio
8. Interest Coverage Ratio
9. Debt to equity Ratio
10. Debt Ratio (D/A)
11. Return on Equity
12. Return on Capital Employed
13. Net profit growth
14. Calculate All
15. Show Calculated Data
0.Exit''')
            n=int(input("Enter choice:\n"))
            if(n==0):
                exit(0)
            if(n==1 or n==14 or n==15):
                self.menu[n](self)
                continue
            name,value=self.menu[n]()
            self.info[name]=value
        return
        


        
        
