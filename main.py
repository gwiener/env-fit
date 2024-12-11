import streamlit as st
import pandas as pd
from scipy.spatial import ConvexHull


st.title("Upper convex hull")
uploaded_file = st.file_uploader(
    "Choose a CSV file with 2 columns, X as the first, Y second, and at least 3 rows",
    type="csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if len(df.columns) != 2:
        st.error("Please upload a file with 2 columns")
        st.stop()
    if len(df) < 3:
        st.error("Please upload a file with more than 2 rows")
        st.stop()
    col0, col1 = df.columns
    st.scatter_chart(df, x=col0, y=col1)
    hull = ConvexHull(df)
    upper_hull = []
    prev_idx = None
    # find only the upper bound
    # SciPy's ConvexHull returns the vertices in counter-clockwise order,
    # so we can check the x coordinate to find the turning point
    for idx in hull.vertices:
        if prev_idx is None:
            upper_hull.append(df.iloc[idx])
        else:
            x0 = df.iloc[prev_idx][col0]
            x1 = df.iloc[idx][col0]
            if x0 > x1:
                upper_hull.append(df.iloc[idx])
        prev_idx = idx
    upper_hull_df = pd.DataFrame(upper_hull)
    st.write("The upper convex hull is:")
    st.scatter_chart(upper_hull_df, x=col0, y=col1)
    orig_file_name = uploaded_file.name
    upper_hull_file_name = orig_file_name.replace(".csv", "_upper_hull.csv")
    download_data = upper_hull_df.to_csv(index=False)
    st.download_button("download upper hull", download_data, file_name=upper_hull_file_name)
