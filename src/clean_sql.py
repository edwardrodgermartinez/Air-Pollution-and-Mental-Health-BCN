import pandas as pd
import numpy as np

def clean_sql (BCN_DATA):
        columns_to_keep = ['occurrence_mental', 'bienestar', 'estres', 'sueno', 'horasfuera', 'enfermo', 'performance', 'z_performance', 'µgm3', 'district', 'sec_noise55_day', 'hours_greenblue_day', 'access_greenbluespaces_300mbuff', 'age_yrs', 'gender']
        BCN_DF = BCN_DATA[columns_to_keep]
        for i in BCN_DF["district"]:
            if i == 'Horta-Guinardo': 
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 29223
            elif i == 'Gràcia':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 33577
            elif i == 'Eixample':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 34770
            elif i == 'Sant Martí':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 30648
            elif i == 'Sants-Montjuïc':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 27350
            elif i == 'Sant Andreu':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 27877
            elif i == 'Sarria Sant-Gervasi':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 49196
            elif i == 'Nou Barris':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 22844
            elif i == 'Les Corts':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 41548
            elif i == 'Ciutat Vella':
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = 22529
            else:
                BCN_DF.loc[BCN_DF["district"] == i, "district_mean_salary"] = None
                
        BCN_DF.to_csv("data/BCN_DF_clean.csv", index = True)
       
import sqlalchemy as alch 

from getpass import getpass
import pandas as pd
import os

def sql_queries ():

    password = getpass()
    dbName = "BCN_DF"
    connectionData=f"mysql+pymysql://root:{password}@localhost/{dbName}"
    engine = alch.create_engine(connectionData)
    
    BCN_DF.to_sql("BCN_DF", if_exists="replace", con=engine, index=False)
    
    
    #SQL Query to look for any patterns in older participants recording more or fewer mental health issues
    query = ''' 
    SELECT
        CASE
            WHEN age_yrs BETWEEN 18 AND 25 THEN '18-25'
             WHEN age_yrs BETWEEN 26 AND 35 THEN '26-35'
            WHEN age_yrs BETWEEN 36 AND 55 THEN '36-55'
            WHEN age_yrs BETWEEN 56 AND 76 THEN '56-76'
        END AS age_group,
        AVG(occurrence_mental),
        AVG(bienestar), 
        AVG(estres), 
        AVG(sueno), 
        AVG(horasfuera)
    FROM
        BCN_DF
    GROUP BY
        age_group
    ORDER BY age_group;
    '''
    pd.read_sql_query(query, engine)
    
    #SQL Query to look for any patterns in men or women recording more or fewer mental health issues
    
    query = ''' 
    SELECT
        gender,
        AVG(occurrence_mental),
        AVG(bienestar), 
        AVG(estres), 
        AVG(sueno),
        AVG(horasfuera)
    FROM
        BCN_DF
    GROUP BY
        gender;
    '''
    pd.read_sql_query(query, engine)
    
    
    #SQL Query to look for patterns in people from different districts reporting more or fewer mental health issues
    
    query = ''' 
    SELECT
        district,
        AVG(occurrence_mental),
        AVG(bienestar), 
        AVG(estres), 
        AVG(sueno),
        AVG(horasfuera)
    FROM
        BCN_DF
    GROUP BY
        district;
    '''
    pd.read_sql_query(query, engine)
    
    
    #SQL Query to look for patterns in people from different districts performing better or worse on the Stroop Test
    
    query = ''' 
    SELECT
        district,
        AVG(performance)
    FROM
        BCN_DF
    GROUP BY
        district;
    '''
    pd.read_sql_query(query, engine)    