import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
                         
def organise(path,period=''):
    '''To read the csv file and organise it;
        Also converts the date and time to the monthly periodic format: M;
        To not change the date to periods,
        enter period=0'''
    data=pd.read_csv(path,header=0,index_col=0,parse_dates=True)
    if(period=="M"):
        data.index=pd.to_datetime(data.index,format="%Y%m",).to_period("M")
        return data
    else:
        return data
    
def ann_return(data,periods_per_year,compound=False):
    '''Gives the annualized returns for a data;
        Returns the annualized return;
        compound=True -> Returns the compound return for the entire period in 1+R format
         '''
    comp_ret=(1+data).prod()
    periods=data.shape[0]
    avg_ret=comp_ret**(1/periods)
    if(compound):
        return comp_ret,((avg_ret)**periods_per_year)-1
    else:
        return ((avg_ret)**periods_per_year)-1

def ann_volatile(data,periods_per_year):
    '''Gives the anualized volatility of the data'''
    vol=data.std(ddof=0)
    return vol*(periods_per_year**(1/2))

def drawdown(returns,principle,category=[]):
    '''Computes the drawdown for the data'''
    if(category):
        wealth_index=principle*((1+returns[category]).cumprod())
    else:
        wealth_index=principle*((1+returns).cumprod())
    prev_peaks=wealth_index.cummax()
    drawdown=(wealth_index-prev_peaks)/prev_peaks
    df=pd.DataFrame({
        'wealth_index':wealth_index,
        'prev_peaks':prev_peaks,
        'drawdowns':drawdown
                    })
    return df,df['drawdowns'].idxmin()

def ff_data_returns(loc):
    data=pd.read_csv(loc)
    data=data[['Lo 10','Hi 10']]
    data.columns=['Small Cap','Large Cap']
    data=data/100
    return data

def skew_kurt(data,ops):
    '''Computes "skewness" - returns the skewness data; and "kurtosis" - returns the kurtosis and excess kurtosis data''' 
    if(ops=='skewness'):
        demean_cube=(data-data.mean())**3
        std_cube=(data.std(ddof=0))**3
        skew_data=demean_cube.mean()/std_cube
        return skew_data
    
    elif(ops=='kurtosis'):
        demean_tofour=(data-data.mean())**4
        std_tofour=(data.std(ddof=0))**4
        kurtosis_data=demean_tofour.mean()/std_tofour
        excess_kurtosis=kurtosis_data-3
        kurt = pd.concat([kurtosis_data,excess_kurtosis],axis='columns')
        kurt.columns=['Kurtosis','Excess Kurtosis']
        return kurt.astype('float')
    else:
        return("Enter the appropriate operation")

def is_normal(data,level=0.02):
    '''Applies the scipy jarque-bera test to check if the data distribution is normal'''
    return stats.jarque_bera(data)[1]>level

def semi_deviation(data):
    '''To calculate the semi-deviation - the deviation in the downside/negative returns portion of the data'''
    return data[data<0].std(ddof=0)

def var_hist(data,level):
    '''Computes the VaR using the exact historical data;
        level = percentage of worst data to be excluded;
        returns the (100-level ) percent VaR'''
    if(isinstance(data,pd.Series)):
        return -(np.percentile(data,level,axis=0))
    elif (isinstance(data,pd.DataFrame)):
        return data.aggregate(var_hist,level=level)
    else:
        raise TypeError("Expected to be DataFrame or Series")

def var_gaussian_param(data,level):
    '''Computes the parametric gaussian var model for the data;
        #This method deduces var by modifying the gaussian distribution based on
        the mean and std of the given data.
        level = the percentsge of worst data to be excluded/
        the percentage at which we are finding VaR'''
    z_gauss=stats.norm.ppf(level/100)
    return -(data.mean()+data.std(ddof=0)*z_gauss)

def cornish_fisher(data,level):
    '''Computes the CF VaR;
        #This method deduces var by modifying the gaussian distribution based on
        the skewness and kurtosis of the given data;
        level = the percentage of worst data to be excluded/
        the percentage at which we are finding VaR'''
    k=skew_kurt(data,'kurtosis')
    s=skew_kurt(data,'skewness')
    z_gauss=stats.norm.ppf(level/100)
    z_data=z_gauss+(z_gauss**2-1)*s/6+(z_gauss**3-3*z_gauss)*(k['Kurtosis']-3)/24-(2*z_gauss**3-5*z_gauss)*(s**2)/36
    return -(data.mean()+data.std(ddof=0)*z_data)

def var_compare(data,level):
    '''Compares the vars deduced by three distinct methods, namely:
        Historical var, Gaussian parametric var and cornish fisher var'''
    var_historical=var_hist(data,level)
    var_gauss=var_gaussian_param(data,level)
    var_cornish=cornish_fisher(data,level)
    var=pd.concat([var_historical,var_gauss,var_cornish],axis=1)
    var.columns=['Historical','Gaussian-Parametric','Cornish-Fisher']
    var.plot.bar(title='VaR Comparison Chart')
    plt.show()
    return

def sharpe_ratio(data,risk_free_rate,periods_per_year):
    '''Computes the sharpe ratio in the following steps:
        1. Takes the excess returns = per_period_return-per_period_rf_return
        2. Annualizes the excess return
        3. Normalizes the ann_excess return by ann_vol
        Input the annual risk free rate(the percentage, without dividing by 100)
        and the periods per year (usually 12 if it is a monthly return)'''
    rf_per_period=(1+risk_free_rate/100)**(1/periods_per_year)-1
    excess_ret=data-rf_per_period
    excess_ret_ann=ann_return(excess_ret,12)
    vol_ann=ann_volatile(data,12)
    return excess_ret_ann[1]/vol_ann

class portfolio:
    '''Input the annual returns as percentages''' 
    def __init__(self,r):
        self.rets=r

    def returns(self,w,assets=[],rets=[]):
        '''
        Computes overall return(weighted average of returns) from the assets comprising the current portfolio.
        Enter the corresponding weights matrix, and the assets in an iteable (not a dictionary). By default all the returns will be used otherwise.
        Returns the return value.
        If you want to enter the return values instead of the assets, give the intended annual rets to 'rets' variable; then the returns will be calculated based on the supplied annual rets data.
        '''
        if(len(assets) and len(rets)):
            raise ValueError("Enter either rets or assets; Can't use both simulataneously")
        
        if(len(assets)!=0):
            try:
                return (w.T @ self.rets[assets])
            except:
                raise ValueError("Weights matrix mismatch. Matrices cannot be multiplied")
        elif(len(rets)):
            try:
                return (w.T@rets)
            except:
                raise ValueError("Weights matrix mismatch. Matrices cannot be multiplied")
        else:
            try:
                return (w.T @ self.rets)
            except:
                raise ValueError("Weights matrix mismatch. Matrices cannot be multiplied")
        return

    def volatile(self,w,cov_mat):
        '''Input the covariance matrix. Returns the overall volatility of the portfolio'''
        try:
            return (w.T @ cov_mat @w)**0.5
        except:
            raise ValueError("Mismatch of weights and covariance matrices")

    def two_asset_folio_analysis(self,assets,points,covmat):
        '''Enter only two assets and the covariance matrix.
            Returns a dataframe containing the weights of the assets, returns, risks and
            the evaluation ratios.
        '''
        if(len(assets)!=2):
            raise ValueError("Enter only two assets to use 'two_asset_folio_analysis' function")
        folio_rets=list()
        folio_vols=list()
        asset_rets_ann=self.rets[assets]
        weights=np.array([[w,1-w] for w in np.linspace(0,1,points)])
        for weight in weights:
            folio_rets.append(self.returns(weight,assets))
            folio_vols.append(self.volatile(weight,covmat))
        folio_rets=np.array(folio_rets)
        folio_vols=np.array(folio_vols)
        asset_1=np.array([w[0] for w in weights])
        asset_2=np.array([w[1] for w in weights])
        df=pd.DataFrame({
            "{}_weight".format(assets[0]):asset_1,
            "{}_weight".format(assets[1]):asset_2,
            "Returns":folio_rets,
            "Volatility":folio_vols,
            "Ret/Vol":folio_rets/folio_vols
            })
        return df

    def two_asset_plot(self,data,axes,style=".-"):
        '''Plots the Returns Vs Risk Efficient frontier for different pairs of weights.
            Input the 2 asset portfolio analysed data that you get after running
            the "two_asset_folio_analysis" function;
            followed by the x and y coordinates respectively, that are to be plotted from the data,
            in an iterable; style=type of graph you want.
        '''
        try:
            data.plot(x=axes[0],y=axes[1],style=style)
            plt.show()
        except:
            print('''Use the "two_asset_folio_analysis" first''')
        return

    def n_asset_ef(self,cov_mat,points,assets=[],plot_ef=False,plot_ew=False,plot_msr=False,plot_cml=False,plot_gmv=False):
        '''
        Gives the optimal weights that constitute the efficient frontier.
        Returns the extra weights of the msr,gmv points, respectively if plot_msr/gmv is set to True.
        plot_ef=False by default; Set True to plot the ef
        assets=[] - calculates for all assets if not specified.
        Note: Set plot_ef to be True in order to get the ewplot,cml,msr and gmv weights.
        '''
        weights_msr=weights_gmv=0
        if(len(assets)==0):
            count=self.rets.shape[0]
            init_guess=np.repeat(1/count,count)
            targets=np.linspace(self.rets.min(),self.rets.max(),points)
        else:
            count=len(assets)
            init_guess=np.repeat(1/count,count)
            targets=np.linspace(self.rets[assets].min(),self.rets[assets].max(),points)
        results=[self.get_ef_weights(init_guess,cov_mat,target,count,assets=assets) for target in targets]
            
        if(plot_ef):
            r_ef=np.array([self.returns(result,assets=assets) for result in results])
            v_ef=np.array([self.volatile(result,cov_mat) for result in results])
            risk_ret=pd.DataFrame({
                'returns':r_ef,
                'risk':v_ef
            })
            ax=risk_ret.plot(x='risk',y='returns',style='.-')
            if(plot_ew):
                weights_ew=np.repeat(1/count,count)
                r_ew=self.returns(weights_ew,assets=assets)
                v_ew=self.volatile(weights_ew,cov_mat)
                ax.plot([v_ew],[r_ew],color='orange',marker='o',markersize=6)
            if(plot_msr):
                weights_msr,rf=self.msr(init_guess,count,cov_mat,assets)
                r_msr=self.returns(weights_msr,assets=assets)
                v_msr=self.volatile(weights_msr,cov_mat)
                ax.plot([v_msr],[r_msr],color='red',marker='d',markersize=7)
                if(plot_cml):
                    cml_x=[0,v_msr]
                    cml_y=[rf,r_msr]
                    ax.plot(cml_x,cml_y,color='yellow',marker='o',markersize=6,linestyle='dashed')
            if(plot_gmv):
                weights_gmv=self.gmv(init_guess,count,cov_mat)
                r_gmv=self.returns(weights_gmv,assets)
                v_gmv=self.volatile(weights_gmv,cov_mat)
                ax.plot([v_gmv],[r_gmv],color='green',marker='o',markersize=6)
            ax.set_xlim(right=0.1,left=0.0)
            plt.show()
            return results,weights_msr,weights_gmv
        else:
            return results
    
    def get_ef_weights(self,init_guess,cov_mat,target,asset_count,assets=[]):
        '''
        Called by the n_asset_ef function.
        This funtion applies the optimizer to minimize the volatility and give optimal weights based on the constraints of:
        (i) Matching the expected/annual return
        (ii) Summing weights to 1
        (iii) Bound weights from 0 to 1
        '''
        bounds=((0.0,1.0),)*asset_count
        verify_target={
            'type':'eq',
            'args':(assets,target),
            'fun':lambda w,assets,target: target-self.returns(w,assets)            
        }
        sum_weights={
            'type':'eq',
            'fun':lambda w: sum(w)-1
        }
        info=minimize(self.volatile,init_guess,args=(cov_mat,),method='SLSQP',constraints=(verify_target,sum_weights),bounds=bounds)
        return info.x

    def msr(self,init_guess,asset_count,cov_mat,assets=[]):
        rf_rate=float(input("Enter the risk free rate as a percentage (for msr calculation): "))
        bounds=((0.0,1.0),)*asset_count
        sum_weights={
            'type':'eq',
            'fun':lambda w: sum(w)-1
        }
        weights=minimize(self.neg_sharpe,init_guess,args=(rf_rate,cov_mat,assets),bounds=bounds,method='SLSQP',constraints=(sum_weights,))
        return weights.x,(rf_rate/100)
        
    def neg_sharpe(self,weights,rf_rate,cov_mat,assets=[],rets=[]):
        rf_rate=rf_rate/100
        r=self.returns(weights,assets=assets,rets=rets)
        risk_adj_r=r-rf_rate
        v=self.volatile(weights,cov_mat)
        return -(risk_adj_r/v)

    def gmv(self,init_guess,asset_count,cov_mat,):
        rf_rate=float(input("Enter the risk free rate as a percentage (for gmv calculation): "))
        bounds=((0.0,1.0),)*asset_count
        sum_weights={
            'type':'eq',
            'fun':lambda w: sum(w)-1
        }
        er=np.repeat(1,asset_count)
        weights=minimize(self.neg_sharpe,init_guess,args=(rf_rate,cov_mat,er),bounds=bounds,method='SLSQP',constraints=(sum_weights,))
        return weights.x 
