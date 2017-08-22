
import tushare as ts
import time
import pandas as pd


# maybe you want to change year and season
cur_year = 2017
cur_season = 1

forcast_year = 2017
forcast_season = 3

###############################################################################################################

# 循环迭代判断每一个值，执行score = score + x, 如第一个值：毛利>=20%时，score +=2
gross_profit_dict = {'20': 2, '30': 1, '40': 1, '60': 1, '70': 1, '80': 1}

# 净利润同比增长
net_profit_growth_dict = {'30': 1, '50': 2, '80': 1, '100': 1, '140': 1, '160': 1, '180': 1, '200': 1, '240': 1,
                          '280': 1}
# 营业收入同比增长
rev_profit_growth_dict = {'10': 1, '20': 1, '30': 1, '40':1, '50': 2, '80': 1, '100': 1, '140': 1, '160': 1, '180': 1,
                          '200': 1, '240': 1, '280': 1}

# reservedPerShare
reservedPerShare_dict = {'0.5': 2, '1': 1, '1.5': 1, '2': 1, '3': 1}

# roe
roe_dict = {'10': 1, '15': 1, '20': 1, '30': 1}

# 每股未分配利润
perundp_dict = {'0.5': 2, '1': 1, '1.5': 1, '2': 1, '3': 1}

# 行业评分字典
industry_dict = {'区域地产': -5, '房地产': -5, '通信行业': 3, '互联网': 3, '半导体': 1, '电信运营': 3, '软件服务': 2, '环境保护': 4}

# type 业绩预告
forcast_dict = {'预盈': 5, '预增': 5, '预升': 5, '预降': -5, '预亏': -5, '预减': -5}


####################################################################################



dateStr = time.strftime("%Y%m%d", time.localtime())

'''
code,代码
name,名称
type,业绩变动类型【预增、预亏等】
report_date,发布日期
pre_eps,上年同期每股收益
range,业绩变动范围
'''
def save_forecast_data():
    forecast_cols = ['股票代码', '预告类型', '预告日期', '变动范围']
    fd = ts.forecast_data(forcast_year, forcast_season)
    del fd['name']
    del fd['pre_eps']
    #fd.columns = forecast_cols;
    fd.to_csv("forecast_%s.csv"%dateStr, encoding="utf-8", index=False)


'''
code,代码
name,名称
industry,所属行业
area,地区
pe,市盈率
outstanding,流通股本(亿)
totals,总股本(亿)
totalAssets,总资产(万)
liquidAssets,流动资产
fixedAssets,固定资产
reserved,公积金
reservedPerShare,每股公积金
esp,每股收益
bvps,每股净资
pb,市净率
timeToMarket,上市日期
undp,未分利润
perundp, 每股未分配
rev,收入同比(%)
profit,利润同比(%)
gpr,毛利率(%)
npr,净利润率(%)
holders,股东人数
'''

def save_stock_basics():
    sb = ts.get_stock_basics()
    #print(sb)
    sb.to_csv("stockbasic_%s.csv" % dateStr, encoding="utf-8", index=True)

def filter():
    sb = pd.read_csv("stockbasic_%s.csv" % dateStr)
    sf = pd.read_csv("forecast_%s.csv"%dateStr)

    t = sb.merge(sf, on="code", how="left")

    # add score column
    t['score'] = 0

    for d in gross_profit_dict.keys():
        t.ix[t['gpr'] >= float(d), 'score'] = t.score + gross_profit_dict[d]

    #for d in roe_dict.keys():
    #    t.ix[t['加权净资产收益率(%)'] >= float(d), 'score'] = t.score + roe_dict[d]

    for d in net_profit_growth_dict.keys():
        t.ix[t['profit'] >= float(d), 'score'] = t.score + net_profit_growth_dict[d]

    for d in rev_profit_growth_dict.keys():
        t.ix[t['rev'] >= float(d), 'score'] = t.score + rev_profit_growth_dict[d]

    for d in reservedPerShare_dict.keys():
        t.ix[t['reservedPerShare'] >= float(d), 'score'] = t.score + reservedPerShare_dict[d]

    for d in perundp_dict.keys():
        t.ix[t['perundp'] >= float(d), 'score'] = t.score + perundp_dict[d]

    for d in forcast_dict.keys():
        t.ix[t['type'] == d, 'score'] = t.score + forcast_dict[d]

    for d in industry_dict.keys():
        t.ix[t['industry'] == d, 'score'] = t.score + industry_dict[d]
    res = t.sort_values(by='score', ascending=False)
    res.to_csv("result_%s.csv"%dateStr, encoding="utf-8", index=False)

#save_stock_basics()
#save_forecast_data()
filter()
