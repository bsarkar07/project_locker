import sys
sys.path.append("D:\MOOC_Material\COURSERA\Portfolio Management with Python")
import returns_analyzer_kit as rak
import pandas as pd
import numpy as np

def arrange(path,name):
    df=rak.organise(path,'M')
    rets=df[['Close']]
    rets=rets/100
    rets.columns=[name]
    rets=rets.pct_change().shift(-1,'M').dropna()
    return rets

mahindra=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Auto\M&M.NS.csv','M&M')
tata=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Auto\TATAMOTORS.NS.csv','Tata Motors')
data=pd.concat([mahindra,tata],axis=1)
data.to_csv(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Auto\auto_rets.csv')
print(data.head(20))

##hcl=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Software\HCLTECH.NS.csv','HCL')
##mahindra=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Software\TECHM.NS.csv','Tech Mahindra')
##wipro=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Software\WIPRO.NS.csv','Wipro')
##df=pd.concat([hcl,mahindra,wipro],axis=1)
##print(df.head(25))
##df.to_csv(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Software\software_rets.csv')


##axis=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\AXISBANK.NS.csv','Axis Bank')
##sbi=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\SBIN.NS.csv','SBI')
##hdfc=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\HDFCBANK.NS.csv','HDFC')
##indus=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\INDUSINDBK.NS.csv','IndusInd')
##kotak=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\KOTAKBANK.NS.csv','Kotak Mahindra')
##icici=arrange(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\ICICIBANK.NS.csv','ICICI')
##data=pd.concat([axis,sbi,hdfc,indus,kotak,icici],axis=1)
##print(data)
##data.to_csv(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\original_price_data\Banks\banks_rets.csv')


