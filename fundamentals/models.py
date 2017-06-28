# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

connect("mongodb://localhost:27017/annaStock")

class StockInfo(MongoModel):
	code = fields.CharField()	# 股票代码
	name = fields.CharField()	# 股票名称
	board = fields.CharField()	# 所在板块
	industry = fields.CharField()		# 行业分类
	area = fields.CharField()			# 所在地区
	ipodate = fields.DateTimeField()	# 上市日期
	
class Report(MongoModel):
	code = fields.CharField()	# 股票代码
	period =  fields.CharField()	# 报告期（一季度、半年报、三季度、年报）
	# income statement
	revenue = fields.BigIntegerField()
	gross_profit = fields.BigIntegerField()
	EBIT = fields.BigIntegerField()
	EBT = fields.BigIntegerField()
	NI = fields.BigIntegerField()
	NI_majority = fields.BigIntegerField()
	NI_recur = fields.BigIntegerField()
	NI_recur_majority = fields.BigIntegerField()
	NI_non_recur = fields.BigIntegerField()
	# balance sheet
	assets = fields.BigIntegerField()
	inventory = fields.BigIntegerField()
	liability = fields.BigIntegerField()
	equity = fields.BigIntegerField()
	# cash flow statement
	CFO = fields.BigIntegerField()
	CFI = fields.BigIntegerField()
	CFF = fields.BigIntegerField()
	# others
	total_stock = fields.BigIntegerField()
	outstanding = fields.BigIntegerField()
	holders = fields.BigIntegerField()
	# per share
	eps_basic = fields.FloatField()
	eps_basic_recur = fields.FloatField()
	eps_diluted = fields.FloatField()
	eps_diluted_recur = fields.FloatField()
	dps = fields.FloatField()
	bvps = fields.FloatField()
	# operating rates
	receivable_turnover = fields.FloatField()
	inventory_turnover = fields.FloatField()

class Rate(MongoModel):
	date = fields.DateTimeField()		# date of adjustment
	name = fields.CharField()			# types of interest rate or bank reserve ratio
	maturity = fields.IntegerField()	# number of months
	value = fields.FloatField()
	last_value = fields.FloatField()
	change = fields.FloatField()

class Macro(MongoModel):
	frequency = fields.CharField()		# 'y' or 'm'
	period = fields.CharField()			# '2017' or '201703'
	# money_supply 
	m2 = fields.BigIntegerField()		# 单位：million
	m2_yoy = fields.FloatField()
	m1 = fields.BigIntegerField()
	m1_yoy = fields.FloatField()
	m0 = fields.BigIntegerField()
	m0_yoy = fields.FloatField()
	cd = fields.BigIntegerField()
	cd_yoy = fields.FloatField()
	qm = fields.BigIntegerField()
	qm_yoy = fields.FloatField()
	ftd = fields.BigIntegerField()
	ftd_yoy = fields.FloatField()
	sd = fields.BigIntegerField()
	sd_yoy = fields.FloatField()
	rests = fields.BigIntegerField()
	rests_yoy = fields.FloatField()
	# gdp
	gdp = fields.BigIntegerField()
	gdp_pc = fields.BigIntegerField()
	gnp = fields.BigIntegerField()
	g1 = fields.BigIntegerField()
	g2 = fields.BigIntegerField()
	industry = fields.BigIntegerField()
	construct = fields.BigIntegerField()
	g3 = fields.BigIntegerField()
	transport = fields.BigIntegerField()
	lbdy = fields.BigIntegerField()
	# cpi
	cpi = fields.FloatField()
	# ppi
	ppi = fields.FloatField()

