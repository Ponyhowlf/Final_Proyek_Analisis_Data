import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_monthly_orders_df(df):
    monthly_orders_df = all_df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return monthly_orders_df

def create_top_5_products_df(df):
    top_5_products_df = df.groupby('product_category_name')quantity_x.sum().sort_values(ascending=False).reset_index()

    return create_top_5_products_df

def create_bottom_5_products_df(df):
    bottom_5_products_df = all_df['product_category_name'].value_counts().tail(5).reset_index()
    bottom_5_products_df.columns = ['product_category_name', 'count']

    return create_bottom_5_products_df

def create_payment_type_sort_df(df):
    payment_type_sort_df = all_df['payment_type'].value_counts(ascending=False)

    return create_payment_type_sort_df

def create_total_revenue_df(df):
    total_revenue_df = all_df['payment_value'].sum()

    return create_total_revenue_df

def create_rfm_df(df):
    rfm_df = all_df.groupby(by="customer_id", as_index=False).agg({
    "order_purchase_timestamp": "max", 
    "order_id": "nunique",
    "payment_value": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
 
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
 
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return create_rfm_df


all_df = pd.read_csv("all_df.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_carrier_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()


st.set_page_config(layout="wide")
 
col1, col2, col3 = st.columns([0.5, 4, 2])
with col1:
    st.image("https://github.com/Ponyhowlf/assets/blob/main/Screenshot%202024-12-08%20at%2022.44.18.png?raw=true", width=100)

with col2:
    st.title('Data Summary and Insights')

with col3:
    start_date, end_date = st.date_input(
        label='Periode',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

    monthly_orders_df = create_monthly_orders_df(main_df)
    top_5_products_df = create_top_5_products_df(main_df)
    bottom_5_products_df = create_bottom_5_products_df(main_df)
    payment_type_sort_df = create_payment_type_sort_df(main_df)
    total_revenue_df = create_total_revenue_df(main_df)
    rfm_df = create_rfm_df(main_df)

    
st.write("\n\n\n")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    ["Monthly Orders",
     " ", "Sold Products",
     " ", "Highest Payment Type",
     " ", "Revenue",
     " ", "Insights" ]
    )

with tab1:
    st.markdown("<h2 style='font-size: 25px; color: #333333;'>Monthly Orders</h2>", unsafe_allow_html=True)

    st.write("\n\n\n")

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        monthly_orders_df["order_purchase_timestamp"],
        monthly_orders_df["order_count"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    
    st.pyplot(fig)


with tab2:
    st.markdown("<h2 style='font-size: 25px; color: #333333;'>Sold Products</h2>", unsafe_allow_html=True)
    st.write("\n\n\n")
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    colors = ["#66b3ff", "#99ff99", "#ffcc99", "#ff99cc", "#66ff66"]

    sns.barplot(x="sales", y="product_category_name", data=top_5_products_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Sales", fontsize=30)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
 
    st.pyplot(fig)
    
    

with tab3:
    st.title("Highest Payment Type")

    plt.figure(figsize=(8, 6))
    plt.bar(all_df['payment_type'], all_df['count'], color=['#66b3ff', '#99ff99', '#ffcc99'])
    
    plt.xlabel('Payment Type',fontstyle='italic')
    plt.ylabel('Count of Orders', fontstyle='italic')
    plt.show()
    






    
