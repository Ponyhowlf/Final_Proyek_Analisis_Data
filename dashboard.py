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

def create_sum_product_category_name_df(df):
    sum_product_category_name_df = (
        df.groupby('product_category_name_english')
        .size()  
        .reset_index(name='category_count') 
        .sort_values(by='category_count', ascending=False)
    )
    return sum_product_category_name_df   

def create_payment_type_sort_df(df):
    payment_type_sort_df = (
        df.groupby('payment_type')
        .size()  
        .reset_index(name='count') 
        .sort_values(by='count', ascending=False)
    )
    return payment_type_sort_df

def create_total_revenue_df(df):
    total_revenue_df = all_df['payment_value'].sum()
    
    return total_revenue_df

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

    return rfm_df


all_df = pd.read_csv("main_data.csv")

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
    payment_type_sort_df = create_payment_type_sort_df(main_df)
    sum_product_category_name_df = create_sum_product_category_name_df(main_df)
    payment_type_sort_df = create_payment_type_sort_df(main_df)
    total_revenue_df = create_total_revenue_df(main_df)
    rfm_df = create_rfm_df(main_df)


    
st.write("\n\n\n")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["Monthly Orders",
     " ", "Sold Products",
     " ", "Payment Type",
     " ", "Insights" ]
    )

with tab1:
    with st.container():
        st.write("\n\n\n")
        st.markdown("<h2 style='text-align: center;'>Monthly Orders</h2>", unsafe_allow_html=True)

        monthly_orders_df['month_name'] = monthly_orders_df['order_purchase_timestamp'].dt.strftime('%B')

        fig, ax = plt.subplots(figsize=(16, 7))

        ax.plot(
            monthly_orders_df["order_purchase_timestamp"],
            monthly_orders_df["order_count"],
            marker='o', 
            linewidth=2,
            color="#90CAF9"
        )
        
        ax.set_xlabel('Time', fontsize=17,labelpad=20)
        ax.set_ylabel('Order', fontsize=17,labelpad=20) 

        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', rotation=45, labelsize=15)

        ax.set_xticks(monthly_orders_df["order_purchase_timestamp"])
        ax.set_xticklabels(monthly_orders_df['month_name'], rotation=45, fontsize=15)
        ax.set_facecolor('#f9f9f9')

    
        st.pyplot(fig)





with tab3:
    with st.container():
    
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))
        
 
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
        sns.barplot(x="category_count", y="product_category_name_english", data=sum_product_category_name_df.head(5), palette=colors, ax=ax[0])
        ax[0].set_ylabel(None)
        ax[0].set_xlabel("Sales", fontsize=20, labelpad=25)
        ax[0].set_title("Top Performing Product", loc="left", fontsize=30, fontweight='bold', pad=25)
        ax[0].tick_params(axis='y', labelsize=20)
        ax[0].tick_params(axis='x', labelsize=20)
        ax[0].set_facecolor('#fafafa')


        sns.barplot(x="category_count", y="product_category_name_english", data=sum_product_category_name_df.sort_values(by="category_count", ascending=True).head(5), palette=colors, ax=ax[1])
        ax[1].set_ylabel(None)
        ax[1].set_xlabel("Sales", fontsize=20, labelpad=25)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Low Performing Product", loc="right", fontsize=30, fontweight='bold', pad=25)
        ax[1].tick_params(axis='y', labelsize=20)
        ax[1].tick_params(axis='x', labelsize=20)
        ax[1].set_facecolor('#fafafa')

        st.pyplot(fig)



with tab5:
    with st.container():
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(16,7))
        ax.bar(
            payment_type_sort_df['payment_type'],
            payment_type_sort_df['count'],
            color=['#90CAF9', '#D3D3D3', '#D3D3D3','#D3D3D3']
            )

        ax.set_title('Distribution of Payment Types', weight='bold', fontsize=30, pad=25)
        ax.set_xlabel('Payment Type', labelpad=20)
        ax.set_ylabel('Count of Orders', labelpad=20)
        ax.set_facecolor('#f9f9f9')

        st.pyplot(fig)


with tab7:
    with st.container():

        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        

        formatted_revenue = format_currency(total_revenue_df, 'USD', locale='en_US')

        st.title(f"Total Revenue: {formatted_revenue}")

        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(y="recency", x="customer_id", hue="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax)

        ax.set_title("By Recency (days)", loc="center", fontsize=20, fontweight='bold', pad=15)

        ax.set_xlabel('Customer ID', fontsize=12, fontstyle='italic', labelpad=15) 
        ax.set_ylabel('Recency (days)', fontsize=12, fontstyle='italic', labelpad=15)

        ax.tick_params(axis ='x', labelsize=9)
        ax.tick_params(axis ='y', labelsize=20)
        ax.set_facecolor('#f9f9f9')

        st.pyplot(fig)


        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)


        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

        colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
        sns.barplot(y="frequency", x="customer_id", hue="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax)

        ax.set_title("By Frequency", loc="center", fontsize=20, fontweight='bold', pad=15)

        ax.set_xlabel('Customer ID', fontsize=12, fontstyle='italic', labelpad=15) 
        ax.set_ylabel('Frequency (times)', fontsize=12, fontstyle='italic', labelpad=15)

        ax.tick_params(axis ='x', labelsize=9)
        ax.tick_params(axis ='y', labelsize=20)
        ax.set_facecolor('#f9f9f9')


        st.pyplot(fig)
        

        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

       

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16, 5))

        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(y="monetary", x="customer_id", hue="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax)

        ax.set_title("By Monetary", loc="center", fontsize=20, fontweight='bold', pad=15)

        ax.set_xlabel('Customer ID', fontsize=12, fontstyle='italic', labelpad=15) 
        ax.set_ylabel('Amount ($)', fontsize=12, fontstyle='italic', labelpad=15)

        ax.tick_params(axis ='x', labelsize=9)
        ax.tick_params(axis ='y', labelsize=20)
        ax.set_facecolor('#f9f9f9')

        st.pyplot(fig)




        



        




    

    
