import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_excel():
	df=pd.read_excel(
		io="customer_product_sales_data.xlsx",
		engine="openpyxl",
		sheet_name="Sales"
	)
	df["rating_count"] = df["rating"].count()
	return df

df = get_data_excel()

print(df)

st.sidebar.header("Please Filter Here:")
Gender = st.sidebar.multiselect(
	"Select the gender:",
	options=df["gender"].unique(),
	default=df["gender"].unique()
)

Marital_Status = st.sidebar.multiselect(
	"Select the marital status:",
	options=df["marital_status"].unique(),
	default=df["marital_status"].unique()
)

Product_Line = st.sidebar.multiselect(
	"Select the product line:",
	options=df["product_line"].unique(),
	default=df["product_line"].unique()
)

Category = st.sidebar.multiselect(
	"Select the product line:",
	options=df["category"].unique(),
	default=df["category"].unique()
)

Country = st.sidebar.selectbox(
	"Select the product line:",
	options=df["country"].unique())

df_selection = df.query(
    "gender == @Gender & marital_status ==@Marital_Status & category == @Category  & country == @Country"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["sls_sales"].sum())
average_rating = round(df_selection["rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["sls_sales"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

sales_by_product_line = df_selection.groupby(by=["product_line"])[["sls_sales"]].sum().sort_values(by="sls_sales")

fig_product_sales = px.bar(
    sales_by_product_line,
    x="sls_sales",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

rating_count = (
    df_selection.groupby("rating")
    .size()
    .reset_index(name="count")
    .sort_values(by="rating")
)

fig_rating = px.bar(
    rating_count,
    x="rating",
    y="count",
    title="<b>Rating Distribution</b>",
    template="plotly_white"
)

fig_rating.update_layout(
    xaxis_title="Rating",
    yaxis_title="Count",
    plot_bgcolor="rgba(0,0,0,0)"
)



sales_by_category = df_selection.groupby(by=["category"])[["sls_sales"]].sum().sort_values(by="sls_sales")

fig_category_sales = px.bar(
    sales_by_category,
    x="sls_sales",
    y=sales_by_category.index,
    title="<b>Sales by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_category),
    template="plotly_white",
)
fig_category_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_rating, use_container_width=True)


sales_by_subcategory = df_selection.groupby(by=["subcategory"])[["sls_sales"]].sum().sort_values(by="sls_sales")

fig_subcategory_pie = px.pie(
    sales_by_subcategory,
    values="sls_sales",
    names=sales_by_subcategory.index,
    title="<b>Sales Distribution by Subcategory</b>",
)

fig_subcategory_pie.update_traces(textinfo='percent+label')


left_column = st.columns(1)[0]
left_column.plotly_chart(fig_subcategory_pie, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)