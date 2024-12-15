import streamlit as st
import pg8000
import pandas as pd
import altair as alt

# Database connection function
def get_db_connection():
    try:
        conn = pg8000.connect(
            host="mini-project.cb460iwoim0p.ap-south-1.rds.amazonaws.com",  # Replace with your PostgreSQL server host
            database="postgres",                                           # Replace with your database name
            user="postgres",                                               # Replace with your username
            password="Password",                                           # Replace with your password
            port="5432"                                                    # Default PostgreSQL port
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to execute a query
def execute_query(query, conn):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

# Function to plot a graph using Altair
def plot_graph(df):
    try:
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(x_col, sort='-y', title=x_col),
                y=alt.Y(y_col, title=y_col),
                tooltip=list(df.columns)
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Not enough data columns to plot a graph.")
    except Exception as e:
        st.error(f"Error plotting graph: {e}")

# Streamlit layout
st.title("Amazon Products Dataset")
st.subheader("Select a predefined query to execute")

# Queries for Page 1 (Guvi Query)
queries_page1 = {
    "1) Find top 10 highest revenue generating products": '''
        SELECT "Product Id", "Category", SUM("Quantity" * "List Price") AS total_revenue
        FROM amazon_products
        GROUP BY "Product Id", "Category"
        ORDER BY total_revenue DESC
        LIMIT 10;
    ''',
    "2) Find the top 5 cities with the highest profit margins": '''
        SELECT "City", 
        CASE WHEN SUM("List Price" * "Quantity") = 0 THEN 0
        ELSE SUM(("List Price" - "cost price") * "Quantity") / SUM("List Price" * "Quantity")
        END AS profit_margin
        FROM amazon_products
        GROUP BY "City"
        ORDER BY profit_margin DESC
        LIMIT 5;
    ''',
    "3) Calculate the total discount given for each category": '''
        SELECT "Category", SUM("Quantity" * "List Price" * "Discount Percent" / 100) AS total_discount
        FROM amazon_products
        GROUP BY "Category";
    ''',
    "4) Find the average sale price per product category": '''
        SELECT "Category", SUM("List Price" * "Quantity") / SUM("Quantity") AS average_sale_price
        FROM amazon_products
        GROUP BY "Category";
    ''',
    "5) Find the region with the highest average sale price": '''
        SELECT "Region", SUM("List Price" * "Quantity") / SUM("Quantity") AS average_sale_price
        FROM amazon_products
        GROUP BY "Region"
        ORDER BY average_sale_price DESC
        LIMIT 1;
    ''',
    "6) Find the total profit per category": '''
        SELECT "Category", SUM(("List Price" - "cost price") * "Quantity") AS total_profit
        FROM amazon_products
        GROUP BY "Category";
    ''',
    "7) Identify the top 3 segments with the highest quantity of orders": '''
        SELECT "Segment", SUM("Quantity") AS total_quantity
        FROM amazon_products
        GROUP BY "Segment"
        ORDER BY total_quantity DESC
        LIMIT 3;
    ''',
    "8) Determine the average discount percentage given per region": '''
        SELECT "Region", AVG("Discount Percent") AS average_discount_percent
        FROM amazon_products
        GROUP BY "Region";
    ''',
    "9) Find the product category with the highest total profit": '''
        SELECT "Category", SUM(("List Price" - "cost price") * "Quantity") AS total_profit
        FROM amazon_products
        GROUP BY "Category"
        ORDER BY total_profit DESC
        LIMIT 1;
    ''',
    "10) Calculate the total revenue generated per year": '''
        SELECT EXTRACT(YEAR FROM CAST("Order Date" AS DATE)) AS year, SUM("List Price" * "Quantity") AS total_revenue
        FROM amazon_products
        GROUP BY year
        ORDER BY year;
    '''
}

# Queries for Page 2 (My Own Query)
queries_page2 = {
    "11) Find the City with the Maximum Number of Orders": '''
        SELECT "City", COUNT(*) AS Total_Orders
        FROM amazon_products
        GROUP BY "City"
        ORDER BY Total_Orders DESC
        LIMIT 1;
    ''',
    "12) Calculate the Average Order Value (AOV) Per Segment": '''
        SELECT "Segment", SUM(("List Price" * "Quantity") * (1 - "Discount Percent" / 100)) / COUNT(*) AS Average_Order_Value
        FROM amazon_products
        GROUP BY "Segment";
    ''',
    "13) Identify the Month with the Highest Total Revenue": '''
        SELECT EXTRACT(MONTH FROM CAST("Order Date" AS DATE)) AS Month, 
        SUM(("List Price" * "Quantity") * (1 - "Discount Percent" / 100)) AS Total_Revenue
        FROM amazon_products
        GROUP BY Month
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    ''',
    "14) Find the Product with the Lowest Total Quantity Sold": '''
        SELECT "Product Id", SUM("Quantity") AS Total_Quantity_Sold
        FROM amazon_products
        GROUP BY "Product Id"
        ORDER BY Total_Quantity_Sold ASC
        LIMIT 1;
    ''',
    "15) Find the Total Revenue for Each City": '''
        SELECT "City", SUM(("List Price" * "Quantity") * (1 - "Discount Percent" / 100)) AS Total_Revenue
        FROM amazon_products
        GROUP BY "City"
        ORDER BY Total_Revenue DESC;
    ''',
    "16) Identify the Product Category with the Most Orders": '''
        SELECT "Category", SUM("Quantity") AS Total_Orders
        FROM amazon_products
        GROUP BY "Category"
        ORDER BY Total_Orders DESC
        LIMIT 1;
    ''',
    "17) Find the Average Discount Percentage Given per Segment": '''
        SELECT "Segment", AVG("Discount Percent") AS Average_Discount_Percent
        FROM amazon_products
        GROUP BY "Segment";
    ''',
    "18) Calculate the Total Quantity Sold Per Ship Mode": '''
        SELECT "Ship Mode", SUM("Quantity") AS Total_Quantity_Sold
        FROM amazon_products
        GROUP BY "Ship Mode"
        ORDER BY Total_Quantity_Sold DESC;
    ''',
    "19) Find the Year with the Highest Total Revenue": '''
        SELECT EXTRACT(YEAR FROM CAST("Order Date" AS DATE)) AS Year, 
        SUM(("List Price" * "Quantity") * (1 - "Discount Percent" / 100)) AS Total_Revenue
        FROM amazon_products
        GROUP BY Year
        ORDER BY Total_Revenue DESC
        LIMIT 1;
    ''',
    "20) Identify the Top 3 Products with the Highest Profit": '''
        SELECT "Product Id", SUM(("List Price" * "Quantity") * (1 - "Discount Percent" / 100) - ("cost price" * "Quantity")) AS Total_Profit
        FROM amazon_products
        GROUP BY "Product Id"
        ORDER BY Total_Profit DESC
        LIMIT 3;
    '''
}

# Dropdown for page selection
page = st.radio("Select Page", ["Guvi Query", "My Own Query"])

# Show the queries based on the selected page
queries = queries_page1 if page == "Guvi Query" else queries_page2
selected_query = st.selectbox("Choose a query to run:", list(queries.keys()))

if st.button("Run Query"):
    query = queries[selected_query]
    conn = get_db_connection()
    if conn:
        df = execute_query(query, conn)
        if df is not None:
            st.success("Query executed successfully!")
            st.write(f"### Results for: {selected_query}")
            st.dataframe(df)  # Display query results
            st.write("### Visualization")
            plot_graph(df)  # Plot the graph
        conn.close()
