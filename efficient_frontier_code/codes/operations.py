import sys
sys.path.append(r"D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\codes")
sys.path.append(r"D:\MOOC_Material\COURSERA\Portfolio Management with Python\Video notebooks_and_codes\nb")
import returns_analyzer_kit as rak
import edhec_risk_kit_109 as erk
import pandas as pd
import numpy as np

def to_rets(path,name):
    df=rak.organise(path,'M')
    rets=df[['Close']]
    rets=rets/100
    rets.columns=[name]
    rets=rets.pct_change().shift(-1,'M').dropna()
    return rets

def operations(data,level):
##    data=pd.read_csv(path,header=0,index_col=0)
    print('Cornish Fisher VaR:')
    print(erk.var_gaussian(data,modified=True))
    print('\nGaussian VaR:')
    print(rak.var_gaussian_param(data,level))
    print('\nHistorical data VaR:')
    print(rak.var_hist(data,level))
    print('\nAnnual Vol:')
    print(rak.ann_volatile(data,12))
    print('\nMax returns over the period since 2016:\n',data.max(),'\nHappened in the y/m:\n',data.idxmax())
    print('\nMin returns over the period since 2016:\n',data.min(),'\nHappened in the y/m:\n',data.idxmin())
    print("\nThe respective Sharpe ratios:\n",rak.sharpe_ratio(data,3,12))
    print('\nSkewness of the data:\n',rak.skew_kurt(data,'skewness'))
    rak.var_compare(data,5)
    return

df=rak.organise(r'D:\MOOC_Material\COURSERA\Portfolio Management with Python\My folio\NSE data\My_folio_rets.csv','M')
data=df['2016':]
sharpes=rak.sharpe_ratio(data,3,12)
print(sharpes)

assets=['Kotak Mahindra','Bharti Airtel','Cipla','Wipro','HDFC']
rets_assets_ann=rak.ann_return(data[assets],12)
cov_assets=data[assets].cov()
my_folio=rak.portfolio(rets_assets_ann)
w_ef,w_msr,w_gmv=my_folio.n_asset_ef(cov_assets,20,assets=assets,plot_cml=True,plot_ef=True,plot_ew=True,plot_msr=True,plot_gmv=True)
my_folio_rets=my_folio.returns(w_gmv,assets=assets)
my_folio_vol=my_folio.volatile(w_gmv,cov_assets)
print("GMV weights: ",w_gmv)
print("Returns with gmv weights: ",my_folio_rets)
print("Annual Vol with gmv weights: ",my_folio_vol*12**0.5)
print("Ret/Risk: ",my_folio_rets/(my_folio_vol*12**0.5))



##var_cornish=rak.cornish_fisher(data,5)
##rak.var_compare(data,5)
##operations(data[['Cipla','Sun Pharma']],5)

    
