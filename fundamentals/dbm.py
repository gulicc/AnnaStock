# -*- coding: utf-8 -*-

from models import Rate, Macro
import tushare as ts
import datetime

# convert tushare returned string to long int
def ts_float(str):
	try:
		f = float(str)
		return f
	except ValueError:
		return 0

# Update Rate collection
Rate.objects.delete()
rlist = []
# get deposit rates
df = ts.get_deposit_rate()
for index,row in df.iterrows():
	if not row['rate']=='--':
		r = Rate(
			date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'), 
			name=row['deposit_type'],
			value=float(row['rate']),
			)
		rlist.append(r)
# get loan rates
df = ts.get_loan_rate()
for index,row in df.iterrows():
	if not row['rate']=='--':
		r = Rate(
			date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'), 
			name=row['loan_type'],
			value=float(row['rate']),
			)
		rlist.append(r)
# get bank reserve ratios
df = ts.get_rrr()
for index,row in df.iterrows():
	r = Rate(
		date=datetime.datetime.strptime(row['date'], '%Y-%m-%d'), 
		name=u'准备金率',
	)
	if not row['now']=='--':
		r.value = float(row['now'])
	if not row['before']=='--':
		r.last_value = float(row['before'])
	if not row['changed']=='--':
		r.change = float(row['changed'])
	rlist.append(r)
# store rates
Rate.objects.bulk_create(rlist)

# update Macro collection
Macro.objects.delete()
mlist = []
# get macro economics data
df1m = ts.get_money_supply()
df1m.set_index('month',append=False,inplace=True,verify_integrity=True)
df1y = ts.get_money_supply_bal()
df1y.set_index('year',append=False,inplace=True,verify_integrity=True)
df2q = ts.get_gdp_quarter()
df2q.set_index('quarter',append=False,inplace=True,verify_integrity=True)
df2q.fillna(0, inplace=True)
df2y = ts.get_gdp_year()
df2y.set_index('year',append=False,inplace=True,verify_integrity=True)
df2y.fillna(0, inplace=True)
df3m = ts.get_cpi()
df3m.set_index('month',append=False,inplace=True,verify_integrity=True)
df4m = ts.get_ppi()
df4m.set_index('month',append=False,inplace=True,verify_integrity=True)
# store macro economics data
for year in range(1980, datetime.datetime.now().year):
	# yearly macro economics data
	m = Macro(frequency='y', period = str(year))
	m_valid = False
	# yearly money supply, index dtype is string
	if m.period in df1y.index:
		m.m2 = long(100*ts_float(df1y.at[m.period,'m2']))		# yearly m2 (million)
		m.m1 = long(100*ts_float(df1y.at[m.period,'m1']))		# yearly m1 (million)
		m.m0 = long(100*ts_float(df1y.at[m.period,'m0']))		# yearly m0 (million)
		m.cd = long(100*ts_float(df1y.at[m.period,'cd']))		# yearly 活期存款 (million)
		m.qm = long(100*ts_float(df1y.at[m.period,'qm']))		# yearly 准货币 (million)
		m.ftd = long(100*ts_float(df1y.at[m.period,'ftd']))		# yearly 定期存款 (million)
		m.sd = long(100*ts_float(df1y.at[m.period,'sd']))		# yearly 储蓄存款 (million)
		m.rests = long(100*ts_float(df1y.at[m.period,'rests']))	# yearly 其他存款 (million)
		m_valid = True
	# yearly gdp, index dtype is int64
	if year in df2y.index:
		m.gdp = long(100*ts_float(df2y.at[year,'gdp']))
		m.gdp_pc = long(100*ts_float(df2y.at[year,'pc_gdp']))
		m.gnp = long(100*ts_float(df2y.at[year,'gnp']))
		m.g1 = long(100*ts_float(df2y.at[year,'pi']))
		m.g2 = long(100*ts_float(df2y.at[year,'si']))
		m.industry = long(100*ts_float(df2y.at[year,'industry']))
		m.construct = long(100*ts_float(df2y.at[year,'cons_industry']))
		m.g3 = long(100*ts_float(df2y.at[year,'ti']))
		m.transport = long(100*ts_float(df2y.at[year,'trans_industry']))
		m.lbdy = long(100*ts_float(df2y.at[year,'lbdy']))
		m_valid = True
	if m_valid == True:
		mlist.append(m)
	# monthly macro economics data
	for month in range(1,13):
		prd = str(year)+'.'+str(month)
		m = Macro(frequency='m',period=prd)
		m_valid = False
		# monthly money supply, index dtype is string
		if m.period in df1m.index:
			m.m2 = long(100*ts_float(df1m.at[m.period,'m2']))	# monthly m2 (million)
			m.m2_yoy = ts_float(df1m.at[m.period,'m2_yoy'])		# monthly m2 yoy
			m.m1 = long(100*ts_float(df1m.at[m.period,'m1']))	# monthly m1 (million)
			m.m1_yoy = ts_float(df1m.at[m.period,'m1_yoy'])		# monthly m1 yoy
			m.m0 = long(100*ts_float(df1m.at[m.period,'m0']))	# monthly m0 (million)
			m.m0_yoy = ts_float(df1m.at[m.period,'m0_yoy'])		# monthly m0 yoy
			m.cd = long(100*ts_float(df1m.at[m.period,'cd']))	# monthly cd (million)
			m.cd_yoy = ts_float(df1m.at[m.period,'cd_yoy'])		# monthly cd yoy
			m.qm = long(100*ts_float(df1m.at[m.period,'qm']))	# monthly qm (million)
			m.qm_yoy = ts_float(df1m.at[m.period,'qm_yoy'])		# monthly qm yoy
			m.ftd = long(100*ts_float(df1m.at[m.period,'ftd']))	# monthly ftd (million)
			m.ftd_yoy = ts_float(df1m.at[m.period,'ftd_yoy'])	# monthly ftd yoy
			m.sd = long(100*ts_float(df1m.at[m.period,'sd']))	# monthly sd (million)
			m.sd_yoy = ts_float(df1m.at[m.period,'sd_yoy'])		# monthly sd yoy
			m.rests = long(100*ts_float(df1m.at[m.period,'rests']))	# monthly rests (million)
			m.rests_yoy = ts_float(df1m.at[m.period,'rests_yoy'])	# monthly rests yoy
			m_valid = True
		# monthly cpi
		if m.period in df3m.index:
			m.cpi = ts_float(df3m.at[m.period,'cpi'])
			m_valid = True
		# monthly ppi
		if m.period in df4m.index:
			m.ppi = ts_float(df4m.at[m.period,'ppi'])
			m_valid = True
		if m_valid == True:
			mlist.append(m)
	# quarterly macro economics data
	for quart in range(1,5):
		prd = str(year)+'.'+str(quart)
		m = Macro(frequency='q',period=prd)
		m_valid = False
		# quarterly gdp, index dtype is float64 (bad api of tushare)
		fprd = float(m.period)
		if fprd in df2q.index:
			m.gdp = long(100*ts_float(df2q.at[fprd,'gdp']))
			m.g1 = long(100*ts_float(df2q.at[fprd,'pi']))
			m.g2 = long(100*ts_float(df2q.at[fprd,'si']))
			m.g3 = long(100*ts_float(df2q.at[fprd,'ti']))
			m_valid = True
		if m_valid == True:
			mlist.append(m)
# end of for year in range(1980,datetime.datetime.now().year):
Macro.objects.bulk_create(mlist)


