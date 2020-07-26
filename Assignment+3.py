# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
#
import pandas as pd
import numpy as np

Energy = pd.read_excel('Energy Indicators.xls', skiprows = 17, skipfooter = 38)

Energy = Energy[['Unnamed: 2', 'Petajoules', 'Gigajoules', '%']]


# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`

Energy.rename(columns = {'Unnamed: 2' : 'Country', 'Petajoules' : 'Energy Supply', 'Gigajoules' : 'Energy Supply per Capita', '%' : '% Renewable'},
              inplace = True)

Energy.replace('...', np.NaN, inplace = True)

Energy['Energy Supply'].astype(np.float64)

# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.

Energy['Energy Supply'] = Energy['Energy Supply']*1000000

#print(Energy['Energy Supply'].dtypes)


# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```

Energy['Country'].replace({"Republic of Korea": "South Korea",
"United States of America20": "United States",
"United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
"China, Hong Kong Special Administrative Region3": "Hong Kong"}, inplace = True)


# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 

def update_country(Country):
	numbers = '0123456789'
	if Country[-1] in numbers:
		Country = Country[:len(Country)-1]
		if Country[-1] in numbers:
			Country = Country[:len(Country)-1]
		return Country
	return Country

def update_country2(Country):
    if '(' in Country:
        return Country.split('(')[0][:-1]
    return Country
        

Energy['Country'] = Energy['Country'].apply(update_country)

Energy['Country'] = Energy['Country'].apply(update_country2)

df1 = Energy.copy()

# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 

GDP = pd.read_csv('world_bank.csv', skiprows = 4)

# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"``

GDP.rename(columns = {'Country Name':'Country'}, inplace = True)

GDP['Country'].replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"}, inplace = True)

df2 = GDP.copy()



# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.

ScimEn = pd.read_excel('scimagojr-3.xlsx')
df3 = ScimEn.copy()

# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 

df = pd.merge(df3.iloc[:15], df2, how = 'inner', on = 'Country')

# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].


df = df[['Rank', 'Country', 'Documents','Citable documents', 'Citations',
       'Self-citations', 'Citations per document', 'H index', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

df = pd.merge(df, df1, how = 'inner', on = 'Country')
df.set_index('Country', inplace = True)

df = df[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
       'Citations per document', 'H index', 'Energy Supply',
        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015']]



# *This function should return a DataFrame with 20 columns and 15 entries.*


# In[ ]:
#print(type(Energy.shape[0] + GDP.shape[0] + ScimEn.shape[0] - 3 * df.shape[0]))

def answer_one():
    return df


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[1]:


#get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[ ]:


def answer_two():
        
        df1 = set(Energy['Country'])
        df2 = set(GDP['Country'])
        df3 = set(ScimEn['Country'])
        union = df1 | df2 | df3
        intersect = df1 & df2 & df3

        return (len(union) - len(intersect))





# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[ ]:


def answer_three():
    Top15 = answer_one()
    avgGDP = Top15.loc[:,'2006':'2015'].mean(axis = 1)
    return avgGDP.sort_values(ascending = False)


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[ ]:


def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15.loc[:,'2006':'2015'].mean(axis = 1)
    #print(Top15['avgGDP'].sort_values(ascending = False))
    country = Top15.sort_values(by ='avgGDP', ascending = False).iloc[5]
    #print(type(country['2006':'2015'].max()- country['2006':'2015'].min()))
    #print(country['2015']- country['2006'])
    return country['2015']- country['2006']



# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[ ]:


def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[ ]:


def answer_six():
    Top15 = answer_one()
    return (Top15['% Renewable'].sort_values(ascending = False).index[0], Top15['% Renewable'].sort_values(ascending = False)[0])




# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[ ]:


def answer_seven():
    Top15 = answer_one()
    Top15['Citation_Ratio'] = Top15['Self-citations']/Top15['Citations']
    return (Top15['Citation_Ratio'].sort_values(ascending = False).index[0], Top15['Citation_Ratio'].sort_values(ascending = False)[0])


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[ ]:


def answer_eight():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    return Top15['PopEst'].sort_values(ascending = False).index[2]



# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[ ]:


def answer_nine():
    Top15 = answer_one()
    
    Top15['Citable docs per Capita'] = Top15['Citable documents']/Top15['PopEst']
    data = Top15[['Citable docs per Capita', 'Energy Supply per Capita']]
    #print(data.corr(method = 'pearson').iloc[0][1])
    
    return data.corr(method = 'pearson').iloc[0][1]



# In[ ]:


def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[ ]:


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[ ]:


def answer_ten():
    Top15 = answer_one()
    Top15['HighRenew'] = [1 if x >= Top15['% Renewable'].median() else 0 for x in  Top15['% Renewable']]
    return Top15['HighRenew'].sort_index()



# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                   'Japan':'Asia', 
                   'United Kingdom':'Europe', 
                   'Russian Federation':'Europe', 
                   'Canada':'North America', 
                   'Germany':'Europe', 
                   'India':'Asia',
                   'France':'Europe', 
                   'South Korea':'Asia', 
                   'Italy':'Europe', 
                   'Spain':'Europe', 
                   'Iran':'Asia',
                   'Australia':'Australia', 
                   'Brazil':'South America'}
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[ ]:


def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                   'United States':'North America', 
                   'Japan':'Asia', 
                   'United Kingdom':'Europe', 
                   'Russian Federation':'Europe', 
                   'Canada':'North America', 
                   'Germany':'Europe', 
                   'India':'Asia',
                   'France':'Europe', 
                   'South Korea':'Asia', 
                   'Italy':'Europe', 
                   'Spain':'Europe', 
                   'Iran':'Asia',
                   'Australia':'Australia', 
                   'Brazil':'South America'}
    
    data = pd.DataFrame(columns = ['Continent','size', 'sum', 'mean', 'std'])
    data['Continent'] = Top15.groupby(ContinentDict).groups.keys()
    data.set_index('Continent', inplace = True)
    data['size'] = Top15.groupby(ContinentDict).agg({'PopEst':np.size})
    data['sum'] = Top15.groupby(ContinentDict).agg({'PopEst':np.sum})
    data['mean'] = Top15.groupby(ContinentDict).agg({'PopEst':np.mean})
    data['std'] = Top15.groupby(ContinentDict).agg({'PopEst':np.std})
    
    
    return data




# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[ ]:


def answer_twelve():
    Top15 = answer_one()
    Top15.reset_index(inplace = True)
    #print(Top15.head())
    #print(Top15.columns)
    Top15['Continent'] = Top15['Country'].map(ContinentDict)
    #print(Top15.head())

    #bins = pd.qcut(Top15['% Renewable'], q=5)
    Top15['bins'] = pd.cut(Top15['% Renewable'], bins=5)
    print(Top15['bins'])
    
    #cut = pd.Categorical(bins, ordered = True)
    #cut = cut.astype(category, bins, ordered = True)
    s = pd.Series(Top15.groupby(['Continent', 'bins'])['Country'].agg(np.count_nonzero))
    s.dropna(inplace = True)
    
    
    
    #Top15['bins'] = pd.qcut(Top15['% Renewable'], q=5)
    #Top15.set_index(['Continent', 'bins'], inplace = True)
    #Top15.sort_index(['Continent', 'bins'], ascending = [], inplace = True)
    print(s.shape)
    #print(pd.qcut(Top15['% Renewable'], q=5))
    #print(Top15.head())
    return s
    
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[ ]:

def update_col(row):
        row = '{:,}'.format(row)
        return row
                
def answer_thirteen():
    Top15 = answer_one()
    return Top15['PopEst'].apply(update_col)




# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[ ]:


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

