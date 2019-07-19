# amsoil_db_utils.py
# credit to http://stackabuse.com/a-sqlite-tutorial-with-python/

import os  
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'amsoil_database.sqlite3')

def db_connect(db_path=DEFAULT_PATH):  
    con = sqlite3.connect(db_path)
    return con




def create_car(con, year, make, model, engine, 
				eng_oil_wgt='', eng_oil_cap='', drain_plug_tq='',
				m_trans1_oil_wgt='', m_trans1_oil_cap='',
				m_trans2_oil_wgt='', m_trans2_oil_cap='',
				m_trans3_oil_wgt='', m_trans3_oil_cap='',
				a_trans1_oil_wgt='', a_trans1_oil_cap='',
				a_trans2_oil_wgt='', a_trans2_oil3_cap='',
				a_trans3_oil_wgt='', a_trans3_oil_cap='',
				front_diff1_oil_wgt='', front_diff1_oil_cap='',
				front_diff2_oil_wgt='', front_diff2_oil_cap='',
				front_diff3_oil_wgt='', front_diff3_oil_cap='',
				rear_diff1_oil_wgt='', rear_diff1_oil_cap='',
				rear_diff2_oil_wgt='', rear_diff2_oil_cap='',
				rear_diff3_oil_wgt='', rear_diff3_oil_cap='',
				trans_case_oil_wgt='', trans_case_oil_cap=''):  
	sql = """
	INSERT INTO cars (year, make, model, engine, eng_oil_wgt, eng_oil_cap, drain_plug_tq,
					  m_trans1_oil_wgt, m_trans1_oil_cap,
					  m_trans2_oil_wgt, m_trans2_oil_cap,
					  m_trans3_oil_wgt, m_trans3_oil_cap,
					  a_trans1_oil_wgt, a_trans1_oil_cap,
					  a_trans2_oil_wgt, a_trans2_oil_cap,
					  a_trans3_oil_wgt, a_trans3_oil_cap,
					  front_diff1_oil_wgt, front_diff1_oil_cap,
					  front_diff2_oil_wgt, front_diff2_oil_cap,
					  front_diff3_oil_wgt, front_diff3_oil_cap,
					  rear_diff1_oil_wgt, rear_diff1_oil_cap,
					  rear_diff2_oil_wgt, rear_diff2_oil_cap,
					  rear_diff3_oil_wgt, rear_diff3_oil_cap,
					  trans_case_oil_wgt, trans_case_oil_cap
					  )
	VALUES (?, ?, ?, ?, ?, ?, ?)"""
	cur = con.cursor()
	cur.execute(sql, (year, make, model, engine, eng_oil_wgt, eng_oil_cap, drain_plug_tq))
	return cur.lastrowid
