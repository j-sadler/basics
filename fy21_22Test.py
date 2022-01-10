# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import pandas as pd
import numpy as np


df22 = pd.read_excel('FY22.xlsx', sheet_name='FY22')
new_header = df22.iloc[0].str.strip()
df22.columns = new_header
df22 = df22[1:]
df22.reset_index(inplace=True)

df22['ind'] = df22['ID #'].astype(str) + '-' + df22['Line Item # [BF Line]'].astype(str)

Status = 'Financed'
Funding_Type = 'BA'
Portfolio = 'Enterprise'
df22.drop('index', axis = 1, inplace = True)

df22 = df22[(df22['Status'] == Status) & (df22['Funding Type'] == Funding_Type) & 
        (df22['Portfolio'] == Portfolio) ]
df22.reset_index(inplace=True)
fy22 = pd.DataFrame()
fy22[['Index', 'Portfolio', 'Congressional Project', 'Sub-Project', 'Sub-Account', 
      'Funding']] = df22[['ind', 'Portfolio', 'Congressional Project', 'Sub-Project', 
                        'Sub-Account', '$ BY OMB Passback Amount' ]]

fy22pt = fy22.pivot_table(values= 'Funding',aggfunc=np.sum, index= ('Congressional Project', 
                                                           'Sub-Project'), columns= 'Sub-Account', fill_value=0)
fy22['FY'] = 'FY22'




df21 = pd.read_excel('FY21.xlsx',sheet_name='FY21')

# 'Portfolio [SPI]'
Portfolio = 'Enterprise'
# DT['Funding Status [SPI]']
FundingStatus = ['Approved','Approved (Non-Target)','Prior Year']
# DT['Funding Type [SPI]']
FundingType = 'BA'

dt21 = df21[(df21['Portfolio [SPI]'] == Portfolio) & (df21['Funding Status [SPI]'].isin(FundingStatus))
            & (df21['Funding Type [SPI]'] == FundingType)]
dt21.reset_index(inplace=True)
fy21 = pd.DataFrame()

fy21[['Index', 'Portfolio' , 'Congressional Project', 'Sub-Project', 'Sub-Account', 
      'Funding']] = dt21[['SPI + Strip # [SPI Strip]', 'Portfolio [SPI]' , 'Congressional Project [SPI]'
     , 'Sub-Project [SPI]', 'Sub-Account [SPI Strip]', '$ Obligated Amount [Req Strip]']]


fy21['FY'] = 'FY21'
fy21['Funding'] = fy21['Funding']/1000000                          
                          
fy21_22 = fy21.append(fy22)                          
                          
fy21_22_pt = fy21_22.pivot_table(values= 'Funding', margins=True,  aggfunc=np.sum, index= ('Congressional Project', 'Sub-Project'), columns= ('FY', 'Sub-Account'), fill_value=0)
    
fy21_22_pt.to_excel('Excel_Sample.xlsx',sheet_name='Sheet1')

g = fy21_22_pt.groupby('Congressional Project')['All'].sum().reset_index(name='sum')      

g2 = fy21_22.groupby(['Congressional Project' , 'Sub-Project'])['Funding'].sum().reset_index(name='sum')

g3 = fy21_22.groupby(['Congressional Project' , 'Sub-Project'])['Funding'].sum()
                