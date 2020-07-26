# In[ ]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[ ]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[ ]:

university_town = pd.DataFrame()
recession = []
housing_data = pd.DataFrame()

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    data = pd.read_csv('university_towns.txt', sep = '\n', header = None)
    state_names = []
    region_names = []
    states = {}

    for value in data[0]:
            if '[ed' in value:
                k = 0
                state = value

            else:
                k = k + 1
                states[state] = k
                region_names.append(value)
        
    for key, value in states.items():
        state_names.extend(((key + '*')*value).split('*')[:-1])
	
    df = pd.DataFrame({'State':state_names, 'RegionName':region_names})
    df['State'] = df['State'].str.replace('\[edit\]', '')
    df['RegionName'] = df['RegionName'].str.replace(' \(.*', '')
    		
    return df



# In[ ]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls', skiprows = 219, usecols = [4,6], names = ['QUARTERS', 'GDP'])
    data['shifted_gdp'] = data['GDP'].shift(1, axis = 0)
    data['change'] = data['GDP'] - data['shifted_gdp']
    data['change'] = [0 if x>0 else 1 for x in data['change']]
    for i in range(len(data['change'])-4):
        quarter = []
        zero_count = 0
        one_count = 0
        for j in range((len(data['change']) - 4)//2):
            if (data['change'].iloc[i+j] == 1):
                quarter.append(data['QUARTERS'].iloc[i + j])
                one_count = one_count + 1
            elif((data['change'].iloc[i+j] == 0) and (len(quarter) > 2) and zero_count < 2):
                quarter.append(data['QUARTERS'].iloc[i + j])
                zero_count = zero_count + 1
            else:
                break
        if (one_count >= 3) and (zero_count ==2):
            recession = quarter
            break
                
    return quarter[0]


# In[ ]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls', skiprows = 219, usecols = [4,6], names = ['QUARTERS', 'GDP'])
    data['shifted_gdp'] = data['GDP'].shift(1, axis = 0)
    data['change'] = data['GDP'] - data['shifted_gdp']
    data['change'] = [0 if x>0 else 1 for x in data['change']]
    for i in range(len(data['change'])-4):
        quarter = []
        zero_count = 0
        one_count = 0
        for j in range((len(data['change']) - 4)//2):
            if (data['change'].iloc[i+j] == 1):
                quarter.append(data['QUARTERS'].iloc[i + j])
                one_count = one_count + 1
            elif((data['change'].iloc[i+j] == 0) and (len(quarter) > 2) and zero_count < 2):
                quarter.append(data['QUARTERS'].iloc[i + j])
                zero_count = zero_count + 1
            else:
                break
        if (one_count >= 3) and (zero_count ==2):
            break
                
    return quarter[-1]


# In[ ]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    data = pd.read_excel('gdplev.xls', skiprows = 219, usecols = [4,6], names = ['QUARTERS', 'GDP'])
    data['shifted_gdp'] = data['GDP'].shift(1, axis = 0)
    data['change'] = data['GDP'] - data['shifted_gdp']
    data['change'] = [0 if x>0 else 1 for x in data['change']]
    for i in range(len(data['change'])-4):
        quarter = []
        zero_count = 0
        one_count = 0
        for j in range((len(data['change']) - 4)//2):
            if (data['change'].iloc[i+j] == 1):
                quarter.append(data['QUARTERS'].iloc[i + j])
                one_count = one_count + 1
            elif((data['change'].iloc[i+j] == 0) and (len(quarter) > 2) and zero_count < 2):
                quarter.append(data['QUARTERS'].iloc[i + j])
                zero_count = zero_count + 1
            else:
                break
        if (one_count >= 3) and (zero_count ==2):
            break
                
    return quarter[-3]


# In[ ]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    data = pd.read_csv('City_Zhvi_AllHomes.csv')
    data['State'].replace(states, inplace = True)
  
    data.set_index(keys = ["State","RegionName"], inplace = True)
    
    data = data.loc[:, '2000-01':'2016-08']
    quarter = 0
    size = len(data.columns)
    
    for i in range(len(data.columns)//3 + 1):
        
        if ((3 * i)+ 2) < size:
            
            #data[data.columns[3*i][:4]+'q'+str((quarter % 4)+1)] = (data[data.columns[3*i]] + data[data.columns[(3*i)+ 1]] + data[data.columns[(3*i)+ 2]])/3
            data[data.columns[3*i][:4]+'q'+str((quarter % 4)+1)] = data.loc[:,data.columns[3*i]:data.columns[(3*i)+ 2]].mean(axis = 1)
            
        elif ((3 * i)+ 1) < size:

            #data[data.columns[3*i][:4]+'q'+str((quarter % 4)+1)] = (data[data.columns[3*i]] + data[data.columns[(3*i)+ 1]])/2
            data[data.columns[3*i][:4]+'q'+str((quarter % 4)+1)] = data.loc[:,data.columns[3*i]:data.columns[(3*i)+ 1]].mean(axis = 1)
            
        else:
  
            data[data.columns[3*i][:4]+'q'+str((quarter % 4)+1)] = data[data.columns[3*i]]
            
        
        quarter = quarter + 1
    data = data.loc[:, '2000q1':'2016q3']
    

    #print(data.index)
    #print(data['2004q4'])
    #print(data.loc[[('Ohio', 'Akron'), ('Ohio', 'Dayton')]].loc[:, ['2010q3', '2015q2', '2016q3']])
    return data


#convert_housing_data_to_quarters()
# In[ ]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    university_town = get_list_of_university_towns()
    
    recession_start = get_recession_start()
    #print(recession_start)
    
    
    
    recession_end = get_recession_end()

    recession_bottom = get_recession_bottom()
    

    housing_data = convert_housing_data_to_quarters()
    
   
    housing_data = housing_data.loc[:,recession_start:recession_bottom]
    housing_data.reset_index(inplace = True)
    
    university_town = pd.merge(housing_data, university_town, how = 'inner', on = ["State", "RegionName"])
    non_university_town = pd.concat([housing_data, university_town]).drop_duplicates(keep = False)
    
    #university_town.set_index(keys = ["State", "RegionName"], inplace = True)
    #university_town.sort_index(inplace = True)

    #non_university_town.set_index(keys = ["State", "RegionName"], inplace = True)
    #non_university_town.sort_index(inplace = True)
    

    #print((university_town[recession_start] /university_town[recession_bottom]).mean())
    #print((non_university_town[recession_start] / non_university_town[recession_bottom]).mean())

    university_town['change'] = university_town[recession_start] /university_town[recession_bottom]
    
    non_university_town['change'] = non_university_town[recession_start] / non_university_town[recession_bottom]
    
    p = ttest_ind(university_town['change'], non_university_town['change'], nan_policy = 'omit')
    #print(p[1])

    if p[1] < 0.01:
        different = True
    else:
        different = False
        
    if (university_town[recession_start] /university_town[recession_bottom]).mean() > (non_university_town[recession_start] / non_university_town[recession_bottom]).mean():
        better = 'non-university town'
    else:
        better = 'university town'

    #print(different, p[1], better)
   
    values = (different, p[1], better,)
    #p_ = 0.005496427353694603
    return (different, p[1], better)

run_ttest()
