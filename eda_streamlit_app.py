# Import necessary libraries
import streamlit as st  # Streamlit for building the app interface
import pandas as pd  # Pandas for data manipulation
import matplotlib.pyplot as plt  # Matplotlib for plotting
import altair as alt  # Altair for interactive charts
from ydata_profiling import ProfileReport  # For generating data profiling reports
import streamlit.components.v1 as components  # To embed HTML reports into Streamlit

# Set the Streamlit page configuration
st.set_page_config(page_title="📊 Interactive EDA App")
st.title("📊 Exploratory Data Analysis (EDA) App")

# Sidebar radio button to let user choose data input method
st.sidebar.header("📂 Data Source")
data_source = st.sidebar.radio("Choose how to load your data:",
                               ["Upload CSV", "Enter Public URL"])

df = None  # Placeholder for the loaded DataFrame

# Option 1: Upload a CSV file manually
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file",
                                             type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

# Option 2: Load data from a public CSV URL
elif data_source == "Enter Public URL":
    url = st.sidebar.text_input("Paste the public CSV URL here")
    if url:
        try:
            df = pd.read_csv(url)
            st.success("Data loaded successfully from URL!")
        except Exception as e:
            st.error(f"Failed to load data from URL: {e}")

# Run only if data has been successfully loaded
if df is not None:
    # Display a preview of the uploaded dataset
    st.write("### Preview of Dataset", df.head())

    # Show basic data properties
    st.subheader("🧮 Dataset Summary")
    st.write(f"Shape: {df.shape}")
    st.write("Missing Values:", df.isnull().sum())

    # Sidebar filter options for categorical columns
    st.sidebar.header("🔍 Filter Data")
    filter_col = st.sidebar.selectbox("Filter by column", df.columns)
    unique_vals = df[filter_col].dropna().unique()
    selected_vals = st.sidebar.multiselect("Select values",
                                           unique_vals,
                                           default=list(unique_vals))
    filtered_df = df[df[filter_col].isin(selected_vals)]
    st.write("### Filtered Data", filtered_df)

    # Allow users to create simple visualizations
    st.subheader("📈 Visualizations")
    chart_type = st.selectbox("Choose a chart type",
                              ["Histogram", "Boxplot", "Scatterplot"])

    # Generate histogram for numeric columns
    if chart_type == "Histogram":
      numeric_cols = df.select_dtypes(include='number').columns
      if len(numeric_cols) == 0:
          st.warning("No numeric columns available for histogram.")
      else:
          col = st.selectbox("Select column", numeric_cols)

          histogram = alt.Chart(df).mark_bar().encode(
              alt.X(col, bin=alt.Bin(maxbins=30), title=f"{col} (binned)"),
              alt.Y('count()', title='Frequency'),
              tooltip=[col]
          ).interactive()

          st.altair_chart(histogram, use_container_width=True)
      
    # Generate boxplot using Altair
    elif chart_type == "Boxplot":
      numeric_cols = df.select_dtypes(include='number').columns
      categorical_cols = df.select_dtypes(exclude='number').columns

      if len(categorical_cols) == 0 or len(numeric_cols) == 0:
          st.warning("You need at least one categorical and one numeric column to draw a boxplot.")
      else:
          x_col = st.selectbox("X Axis (categorical)", categorical_cols)
          y_col = st.selectbox("Y Axis (numeric)", numeric_cols)

          boxplot = alt.Chart(df).mark_boxplot().encode(
              x=alt.X(x_col, type='nominal'),
              y=alt.Y(y_col, type='quantitative'),
              tooltip=[x_col, y_col]
          ).interactive()

          st.altair_chart(boxplot, use_container_width=True)

    # Generate scatterplot for two numeric columns
    elif chart_type == "Scatterplot":
      x = st.selectbox("X-axis", df.select_dtypes(include='number').columns, key="scatter_x")
      y = st.selectbox("Y-axis", df.select_dtypes(include='number').columns, key="scatter_y")

      scatter_chart = alt.Chart(df).mark_circle(size=60).encode(
          x=alt.X(x, type='quantitative'),
          y=alt.Y(y, type='quantitative'),
          tooltip=[x, y]
      ).interactive()

      st.altair_chart(scatter_chart, use_container_width=True)

    # Display full profiling report using ydata-profiling
    st.subheader("📋 Data Profiling Report")
    profile = ProfileReport(df, title="Data Profile Report", explorative=True)
    components.html(profile.to_html(), height=1000, scrolling=True)

    # Allow user to download the filtered data as a CSV file
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data", csv, "filtered_data.csv",
                       "text/csv")

# If no data has been loaded, display an instructional message
else:
    st.info("Please upload a file or enter a public URL to begin.")












