# -*- coding: utf-8 -*-

from models import StockInfo, Report
import tushare as ts
import datetime
import math
import traceback

# Update StockInfo collection
StockInfo.objects.delete()
stocklist = []
# get stock basics
df = ts.get_stock_basics()
for index, row in df.iterrows():
	s = StockInfo(
		code = unicode(index, 'utf-8'),
		name = unicode(row['name'],'utf-8'),
		industry = unicode(row['industry'],'utf-8'),
		area = unicode(row['area'],'utf-8'),
		)
	intdate = row['timeToMarket']
	if intdate > 0:
		intyear = intdate/10000
		intmonth = (intdate-intyear*10000)/100
		intday = intdate-intyear*10000-intmonth*100
		s.ipodate = datetime.datetime(intyear, intmonth, intday)
	stocklist.append(s)
StockInfo.objects.bulk_create(stocklist)

# Update Report collection
Report.objects.delete()
for year in range(2000, datetime.datetime.now().year):
#for year in range(2010,2011):
	for quarter in range(1,5):
		prd = str(year)+'.'+str(quarter)
		rdict = {}
		try:
			df1 = ts.get_report_data(year,quarter)
			for index, row in df1.iterrows():
				r = Report(code=row['code'], period=prd)
				r_valid = False
				if not math.isnan(row['eps']):
					r.eps_basic = row['eps']
					r_valid = True
				if not math.isnan(row['bvps']):
					r.bvps = row['bvps']
					r_valid = True
				if not math.isnan(row['net_profits']):
					r.NI = long(10000*row['net_profits'])
					r_valid = True
				if r_valid == True:
					rdict[r.code] = r
		except:
			print('Failure: get_report_data @'+prd)

		try:
			df2 = ts.get_profit_data(year,quarter)
			for index, row in df2.iterrows():
				if row['code'] in rdict:
					r = rdict[row['code']]
					if not math.isnan(row['business_income']):
						r.revenue = long(1000000*row['business_income'])
				else:
					r = Report(code=row['code'],period=prd)
					if not math.isnan(row['business_income']):
						r.revenue = long(1000000*row['business_income'])
						rdict[r.code] = r
		except:
			print('Failure: get_profit_data @'+prd)

		try:
			df3 = ts.get_operation_data(year,quarter)
			for index, row in df3.iterrows():
				if row['code'] in rdict:
					r = rdict[row['code']]
					if not math.isnan(row['inventory_turnover']):
						r.inventory_turnover = row['inventory_turnover']
					if not math.isnan(row['arturnover']):
						r.receivable_turnover = row['arturnover']
				else:
					r = Report(code=row['code'],period=prd)
					r_valid = False
					if not math.isnan(row['inventory_turnover']):
						r.inventory_turnover = row['inventory_turnover']
						r_valid = True
					if not math.isnan(row['arturnover']):
						r.receivable_turnover = row['arturnover']
						r_valid = True
					if r_valid == True:
						rdict[r.code] = r
		except:
			print('Failure: get_operation_data @'+prd)

		rlist = rdict.values()
		Report.objects.bulk_create(rlist)
