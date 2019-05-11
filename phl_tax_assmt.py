import pandas as pd
import os

rel_path = r'./'
file_name = 'opa_properties_public.csv' # downloaded from OpenDataPhilly
out_file = 'phl_tax_assmt_ratio.csv'

df = pd.read_csv(os.path.join(rel_path, file_name))

# Keeping only the required columns
df_trunc = df[['category_code_description','market_value','parcel_number','sale_date','sale_price',
               'total_area','taxable_building','taxable_land','zip_code','zoning','lat','lng']]

# Keeping only the recent sales (Jan 2018 onwards) with Sale Price >= $10,000
df_trunc = df_trunc[(df_trunc['sale_date'].astype(str).str[:4] >= '2018') &
                    (df_trunc['sale_price'] >= 10000)]
df_trunc = df_trunc[df_trunc['category_code_description'] == 'Single Family']

# Calculating the Total Assessment (land + building), and the Sales Ratio
df_trunc['tax_assessment'] = df_trunc['taxable_building'] + df_trunc['taxable_land']
df_trunc['sales_ratio'] = df_trunc['tax_assessment']/df_trunc['sale_price']

# Creating Sales Ratio Categories for Interactive Map Visualization
def ratio_catg(ratio):
    if ratio >= 2.0:
        catg = 1
    elif ratio >= 1.5:
        catg = 2
    elif ratio >= 1.2:
        catg = 3
    elif ratio >= 1.05:
        catg = 4
    elif ratio >= 0.95:
        catg = 5
    elif ratio >= 0.8:
        catg = 6
    elif ratio >= 0.65:
        catg = 7
    elif ratio >= 0.5:
        catg = 8
    else:
        catg = 9
    return catg

df['ratio_catg'] = df['sales_ratio'].apply(ratio_catg)

# Saving the processed dataset as a CSV - to be used to create a Tileset
df.to_csv(os.path.join(rel_path,outfile))
