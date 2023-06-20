import pandas as pd

# Load the datasets
actuals_df = pd.read_csv('actuals.csv')
target_df = pd.read_csv('targets.csv')
price_df = pd.read_csv('price.csv')
bcr_df = pd.read_csv('bcr.csv')

# Clean and consolidate the actuals data
consolidated_actuals_df = actuals_df.merge(price_df, on=['Material Description', 'Plant'])
consolidated_actuals_df['Bottle Rands'] = consolidated_actuals_df['Bottle Price'] * consolidated_actuals_df['Quantity']
consolidated_actuals_df['Crate Rands'] = consolidated_actuals_df['Crate Price'] * consolidated_actuals_df['Quantity']

# Variance analysis
variance_df = pd.merge(consolidated_actuals_df, target_df, on=['Year', 'Period', 'Plant', 'Material Number'], suffixes=('_Actuals', '_Target'))
variance_df['Variance'] = variance_df['Actuals'] - variance_df['Target Quantity']

# Actuals & Target analysis by Plant
plant_analysis_df = consolidated_actuals_df.groupby('Plant').agg({'Actuals': 'sum', 'Target Quantity': 'sum'})

# Actuals, Target & Variance analysis by Plant & Category
category_analysis_df = consolidated_actuals_df.groupby(['Plant', 'Category']).agg({'Actuals': 'sum', 'Target Quantity': 'sum'})
category_analysis_df['Variance'] = category_analysis_df['Actuals'] - category_analysis_df['Target Quantity']

# Trend analysis for each Category & Plant
trend_analysis_df = consolidated_actuals_df.groupby(['Category', 'Plant']).agg({'Actuals': 'sum'})

# Print the results
print("Consolidated Actuals Data:")
print(consolidated_actuals_df)

print("\nVariance Analysis:")
print(variance_df)

print("\nActuals & Target Analysis by Plant:")
print(plant_analysis_df)

print("\nActuals, Target & Variance Analysis by Plant & Category:")
print(category_analysis_df)

print("\nTrend Analysis for each Category & Plant:")
print(trend_analysis_df)
