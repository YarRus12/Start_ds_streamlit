import pandas as pd

COVID = pd.read_csv('Covid Data.csv')
male_df = COVID[COVID['SEX'] == 1]
# Создание нового столбца с диапазонами возраста на основе целочисленных значений
bins = [0, 18, 35, 55, 100]
labels = ['0-18', '19-34', '35-54', '55+']
male_df['AGE_RANGE'] = pd.cut(male_df['AGE'], bins=bins, labels=labels, include_lowest=True)
age_range_counts = male_df['AGE_RANGE'].value_counts()

male_df = male_df.merge(age_range_counts.to_frame().rename(columns={'AGE_RANGE': 'COUNT'}), left_on='AGE_RANGE', right_index=True)
print(male_df)


