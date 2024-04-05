import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

CHOSEN_DATA = ["Пневмония", "Беременность"]

@st.cache_data(ttl=60 * 60 * 24)
def create_schedule_main(dataframe) -> None:
    male_df = dataframe[dataframe['SEX'] == 1]
    # Создание нового столбца с диапазонами возраста на основе целочисленных значений
    bins = [0, 18, 35, 55, 100]
    labels = ['0-18', '19-34', '35-54', '55+']
    male_df['AGE_RANGE'] = pd.cut(male_df['AGE'], bins=bins, labels=labels, include_lowest=True)
    age_range_counts = male_df['AGE_RANGE'].value_counts()

    male_df['count'] = male_df['AGE_RANGE'].map(age_range_counts)
    res_male = male_df[['AGE_RANGE', 'count']].drop_duplicates()
    st.table(res_male)

    st.write("")
    bar_chart = alt.Chart(male_df).mark_bar().encode(
        x=alt.X('AGE_RANGE:O', axis=alt.Axis(title='Возрастные группы', labelAngle=0, tickMinStep=1)),  # Ось x - годы
        y=alt.Y(f'count:Q', axis=alt.Axis(title='Число пациентов мужского пола', tickMinStep=5))  # Ось y - ВВП в трлн руб.
    ).properties(
        width=1000,  # Ширина графика
        height=400  # Высота графика
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.text('Очень странныя выборка')

if __name__ == '__main__':
    data = pd.read_csv('Covid Data.csv')
    min_age = data['AGE'].min()
    max_age = data['AGE'].max()
    man_count = data['SEX'].max
    PNEUMONIA_number = data[data['PNEUMONIA'] == 1].shape

    st.title('Просто проект, пусть будет про COVID-19')
    data['DATE_DIED'] = data['DATE_DIED'].replace('9999-99-99', '01/01/2099')
    data['DATE_DIED'] = pd.to_datetime(data['DATE_DIED'], format='%d/%m/%Y')

    # Извлечение года и месяца
    data['year_died'] = data['DATE_DIED'].dt.year
    data['month_died'] = data['DATE_DIED'].dt.month

    min_data = data['month_died'].min()
    max_data = data['year_died'].max()
    st.write("")

    selected_activity = st.multiselect(
        'Какие нибудь особенные данные?',
        options=CHOSEN_DATA, default=CHOSEN_DATA
    )
    st.write("")

    for record in range(len(selected_activity)):
        if selected_activity[record] == 'Пневмония':
            selected_activity[record] = 'PNEUMONIA'
        if selected_activity[record] == 'Беременность':
            selected_activity[record] = 'PREGNANT'

    from_year, to_year = st.slider(
        'Какой возраст заболевших?',
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age))
    st.write("")

    filtered_df = data[
        (data['AGE'] <= to_year)
        & (from_year <= data['AGE'])
        ]
    for x in selected_activity:
        filtered_df = filtered_df[(filtered_df[x] == 1)]

    st.write("")
    st.write("")

    create_schedule_main(filtered_df)

    st.sidebar.markdown(
        """
        <style>
        .sidebar-title {
            text-align: center;
        }
        </style>
        <h1 class="sidebar-title"> Привет 👋 </h1>
        <h1 class="sidebar-title"> Это просто приложение для прохождения урока)))</h1> 
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2LSQ6NW6svZeQF9r_hSeOXPZVJsDo8DGuWmJw5pLehCT1iSiSp9mLHuSfIBGuHPdmOTI&usqp=CAU" width="100%">
        """,
        unsafe_allow_html=True
    )

