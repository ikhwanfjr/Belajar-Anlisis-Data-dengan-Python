import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_weather_reg_df(df):
    weather_reg_df = df.groupby(['weathersit']).registered.sum().sort_values(ascending=False).reset_index()

    if not (weather_reg_df['weathersit'] == 4).any():
        new_idx = pd.DataFrame({"weathersit": [4], "registered": [0]})
        weather_reg_df = pd.concat([weather_reg_df, new_idx], ignore_index=True)

    weather_reg_df.rename(columns={
        "weathersit": "weathers",
        "registered": "registered_customer"
    }, inplace=True)

    return weather_reg_df

def create_hr_reg_df(df):
    hr_reg_df = df.groupby(['hr']).registered.sum().reset_index()
    hr_reg_df.rename(columns={
        'hr': 'hour',
        'registered': 'registered_customer'
    }, inplace=True)

    return hr_reg_df

day_df = pd.read_csv("https://raw.githubusercontent.com/ikhwanfjr/Belajar-Anlisis-Data-dengan-Python/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/ikhwanfjr/Belajar-Anlisis-Data-dengan-Python/main/data/hour.csv")

column = "dteday"
day_df.sort_values(by=column, inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by=column, inplace=True)
hour_df.reset_index(inplace=True)

day_df[column] = pd.to_datetime(day_df[column])
hour_df[column] = pd.to_datetime(hour_df[column])

min_date = day_df[column].min()
max_date = day_df[column].max()

with st.sidebar:
    st.image("https://st2.depositphotos.com/40527348/44435/v/450/depositphotos_444356130-stock-illustration-bicycle-rental-icons-set-logo.jpg")

    # Mengambil start_date dan end_date
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df[column] >= str(start_date)) & 
                (day_df[column] <= str(end_date))]
sec_df = hour_df[(hour_df[column] >= str(start_date)) & 
                (hour_df[column] <= str(end_date))]

weather_reg_df = create_weather_reg_df(main_df)
hr_reg_df = create_hr_reg_df(sec_df)

st.header('Bike Sharing Dashboard :sparkles:')

# Visualisasi Pertanyaan 1
st.subheader("pengguna Terdaftar (Anggota) Menyewa Sepeda Berdasarkan Cuaca")

fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(
    x="weathers", 
    y="registered_customer",
    data=weather_reg_df.sort_values(by="registered_customer", ascending=False),
    palette='deep',
    ax=ax
)
ax.set_title("Jumlah Pengguna Terdaftar Menyewa Sepeda Berdasarkan Faktor Cuaca", loc="center", fontsize=30)
ax.set_ylabel('Jumlah Pengguna Terdaftar (x1.0000.000)', fontsize=20)
ax.set_xlabel('Kondisi Cuaca', fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=20)
ax.set_xticklabels(['Cerah', 'Mendung', 'Hujan Kecil', 'Hujan Lebat'])
st.pyplot(fig)

# Visualisasi Pertanyaan 2
st.subheader("pengguna Terdaftar (Anggota) Menyewa Sepeda Berdasarkan Jam")

fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(
    x="hour", 
    y="registered_customer",
    data=hr_reg_df,
    palette='muted',
    ax=ax
)
ax.set_title("Jumlah Pengguna Terdaftar Menyewa Sepeda Berdasarkan Jam", loc="center", fontsize=30)
ax.set_ylabel('Jumlah Pengguna Terdaftar', fontsize=20)
ax.set_xlabel('Jam Dalam Sehari (00.00 - 23.00)', fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

