import pandas as pd
import numpy as np
import sqlalchemy as alch 
from getpass import getpass
import pandas as pd
import os
from src import clean_sql

BCN_DATA = pd.read_csv('data/BCN_DATA.csv')

clean_sql.clean_sql(BCN_DATA)

