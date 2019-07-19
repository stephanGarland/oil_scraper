# AMSOIL web scraper
# The switching between single and double quotes in some instances, such as 
# the try blocks for element and the select_by_xpath
# is deliberate, as it doesn't work unless they're set like that
# Given that this is a temporary tool, it's not a priority to make it prettier

from amsoil_db_utils import create_car, db_connect
from json import dumps
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import re
import sqlite3
import time

logpath = os.path.join(os.path.dirname(__file__), 'amsoil_log.txt')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', filename=logpath)
logExc = logging.getLogger("ex")
logging.info("Begin")
con = db_connect()
cur = con.cursor()
init_sql = """
	CREATE table IF NOT EXISTS cars (
		id integer PRIMARY KEY,
		year integer NOT NULL,
		make text NOT NULL,
		model text NOT NULL,
		engine text NOT NULL,
		eng_oil_wgt text,
		eng_oil_cap real,
		drain_plug_tq integer,
		m_trans_oil_cap real,
		a_trans_oil_cap real,
		front_diff_oil_wgt text,
		front_diff_oil_cap real,
		cen_diff_oil_wgt text,
		cen_diff_oil_cap real,
		rear_diff_oil_wgt text,
		rear_diff_oil_cap real,
		trans_case_oil_wgt text,
		trans_case_oil_cap real)
		"""
cur.execute(init_sql)

browser = webdriver.Chrome()
browser.get("https://www.amsoil.com/lookup/auto-and-light-truck/")

year_list = []
make_list = []
model_list = []
engine_list = []

i = 0
j = 0
k = 0
l = 0



def get_selection(param):
	selection = browser.find_element_by_xpath("//select[@id='" + param + "']")
	return selection



def get_options(param):
	options = param.find_elements_by_tag_name("option")
	return options



select_year = get_selection('year')
options_year = get_options(select_year)


for option in options_year: #iterate over the options, place attribute value in list
	year_list.append(option.get_attribute("value"))
# Remove first blank element from list
# normally [0] but to delete 2019, since there are no recommendations for it on the site, [:2]
del year_list[:2]

for option_value in year_list:
	select_year = get_selection('year')
	options_year = get_options(select_year)
	print("Looping through years: {}".format(option_value))
	

	select_year = Select(browser.find_element_by_xpath('//select[@id="year"]'))
	select_year.select_by_value(option_value)
	i += 1
	if i == len(year_list) + 1:
		i = 0
		break
	current_year = option_value

	try:
		element = WebDriverWait(browser, 5).until(
		EC.presence_of_element_located((By.XPATH, '//*[@id="make"]')))
		# Sleep is needed for the other menus to load
		time.sleep(0.5)
	except Exception:
		pass

	select_make = get_selection('make')
	options_make = get_options(select_make)
	# have to re-init the list so the next run doesn't append to the previous
	make_list = []
	
	for option in options_make:
   		make_list.append(option.get_attribute("value"))
	del make_list[0]

	for option_value in make_list:
		select_make = get_selection('make')
		options_make = get_options(select_make)
		print("Looping through makes: {}".format(option_value))
		# necessary to prevent stale element exceptions
		time.sleep(0.5)

		select_make = Select(browser.find_element_by_xpath('//select[@id="make"]'))
		select_make.select_by_value(option_value)
		j += 1
		if j == len(make_list) + 1:
			j = 0
			break
		current_make = option_value
		
		try:
			element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="model"]')))
			time.sleep(0.5)
		except Exception:
			pass

		select_model = get_selection('model')
		options_model = get_options(select_model)
		model_list = []

		for option in options_model:
	   		model_list.append(option.get_attribute("value"))
		del model_list[0]

		for option_value in model_list:
			select_model = get_selection('model')
			options_model = get_options(select_model)
			print("Looping through models: {}".format(option_value))
			time.sleep(0.5)
			select_model = Select(browser.find_element_by_xpath('//select[@id="model"]'))
			select_model.select_by_value(option_value)
			k += 1
			if k == len(model_list) + 1:
				k = 0
				break
			current_model = option_value

			try:
				element = WebDriverWait(browser, 5).until(
				EC.presence_of_element_located((By.XPATH, '//*[@id="engine"]')))
				time.sleep(0.5)
			except Exception:
				pass

			select_engine= get_selection('engine')
			options_engine = get_options(select_engine)
			engine_list = []

			for option in options_engine:
				engine_list.append(option.get_attribute("value"))
			del engine_list[0]

			for option_value in engine_list:
				select_engine= get_selection('engine')
				options_engine = get_options(select_engine)
				print("Looping through engines: {}".format(option_value))
				time.sleep(0.5)
				select_engine = Select(browser.find_element_by_xpath('//select[@id="engine"]'))
				select_engine.select_by_value(option_value)
				l += 1
				if l == len(engine_list) + 1:
					l = 0
					break
				current_engine = option_value

				try:
					element = WebDriverWait(browser, 2).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="engine"]')))
				except Exception:
					pass

				url_to_pass = 'https://www.amsoil.com/lookup/auto-and-light-truck/' +\
							current_year + '/' +\
							current_make + '/' +\
							current_model + '/' +\
							current_engine + '/' +\
							'us-volume/'
				# json.dumps converts the Python string to a JS string	
				browser.execute_script("window.open(" +
									  dumps(url_to_pass) + ")")
				browser.switch_to.window(browser.window_handles[1])
				try:
					element = WebDriverWait(browser, 5).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="engine1"]')))
					time.sleep(0.5)
				except Exception:
					pass

				# XPaths containing information we need
				try:
					select_engine_oil = browser.find_element_by_xpath("//*[contains(text(), 'Viscosities')]/following-sibling::span")
					select_capacity_engine_oil = browser.find_element_by_xpath("//*[contains(text(), 'With filter')]")
					select_drain_plug_torque = browser.find_element_by_xpath("//*[contains(text(), 'Oil Drain Plug')]")

					engine_oil_weight = select_engine_oil.text
					capacity_engine_oil = select_capacity_engine_oil.text
					drain_plug_torque = select_drain_plug_torque.text

					strip_weight_regex = r".*?(\d+W-\d+).*"
					strip_capacity_regex = r".*?(\d+.\d+|\d+).*"
					strip_torque_regex = r".*?(\d+.\d+|\d+).*"
					subst_regex = "\\1"

					current_eng_oil_wgt = re.sub(strip_weight_regex, subst_regex, engine_oil_weight, 0, re.M)
					current_eng_oil_cap = re.sub(strip_capacity_regex, subst_regex, capacity_engine_oil, 0, re.M)
					current_drain_plug_tq = re.sub(strip_torque_regex, subst_regex, drain_plug_torque, 0, re.M)

				# some vehicles don't have any recommended oil yet; ignore them for now
				except NoSuchElementException:
					logging.info("No data available for {0} {1} {2} with {3}".format(current_year, current_make, current_model, current_engine))
					pass
				#time.sleep(1)
				browser.find_element_by_partial_link_text('Transmission').click();
				time.sleep(10)
				try:
					print("Writing new row for {0} {1} {2} with {3}".format(current_year, current_make, current_model, current_engine))
					#create_car(con, current_year, current_make, current_model, current_engine, current_eng_oil_wgt, current_eng_oil_cap, current_drain_plug_tq)
					#con.commit()
				except:
					#con.rollback()
					log.exception("Error!")
				# Ensures that we won't grab more than 10/minute
				time.sleep(5)
				browser.close()
				browser.switch_to.window(browser.window_handles[0])
				
con.close()
logging.info("Finish")