import pandas as pd
import os

project_path = os.getcwd()
data_path = os.path.join(project_path, 'data.xlsx')
salesData = pd.read_excel(data_path, sheet_name='SalesData')
salesPersonData = pd.read_excel(data_path, sheet_name='SalespersonData')

country_SD_3 = salesData[['日期', '国家', '销售额', '利润']].groupby([salesData['日期'].dt.year, '国家']).agg({'销售额': 'sum', '利润' : 'sum'})
country_SD_3.head(3)

# task 1.1
pivoted_data = country_SD_3.pivot_table(values=['销售额', '利润'], columns=['日期'], index='国家')

pivoted_data.columns = pivoted_data.columns.rename(['指标', '日期'])
# 获取列名（年份）
years = pivoted_data.columns

# 创建新的 MultiIndex 列，用于存放增长率
new_columns = pd.MultiIndex.from_product(
    [['销售额年增长率', '利润年增长率'], pivoted_data.columns.levels[1]],
    names=['指标', '日期']
)

# 初始化增长率数据框，与 pivoted_data 具有相同的行索引和新创建的增长率列
growth_rates = pd.DataFrame(index=pivoted_data.index, columns=new_columns)

# 计算增长率并存入 growth_rates 数据框
for country in pivoted_data.index:
    for year in pivoted_data.columns.levels[1][1:]:  # 从第二年开始计算增长率
        # 获取销售额和利润的当前年和上一年的数据
        current_sales = pivoted_data.loc[country, ('销售额', year)]
        current_profit = pivoted_data.loc[country, ('利润', year)]
        prev_sales = pivoted_data.loc[country, ('销售额', year - 1)]
        prev_profit = pivoted_data.loc[country, ('利润', year - 1)]
        
        # 计算增长率
        sales_growth = (current_sales - prev_sales) / prev_sales * 100 if prev_sales != 0 else None
        profit_growth = (current_profit - prev_profit) / prev_profit * 100 if prev_profit != 0 else None
        
        # 将增长率存入相应位置
        growth_rates.loc[country, ('销售额年增长率', year)] = sales_growth
        growth_rates.loc[country, ('利润年增长率', year)] = profit_growth

# 将增长率数据合并到原始数据框中
pivoted_data = pd.concat([pivoted_data, growth_rates], axis=1)
print(pivoted_data.sort_values(by=('销售额',2020), ascending=False)[[('销售额', 2020), ('销售额年增长率', 2020), ('利润年增长率', 2020)]].head(3))

# task 1.2
services = salesData[['国家', '地区', '服务分类', '销售额', '利润']].groupby(['地区', '服务分类']).agg({'销售额': 'sum', '利润' : 'sum'})
print(services)
