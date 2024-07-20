import streamlit as st
import pandas as pd
import io
from datetime import datetime


def process_files(uploaded_files):
    try:
        results = []

        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "text/csv":
                    df = pd.read_csv(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    df = pd.read_excel(uploaded_file)

                file_result = {"File": uploaded_file.name}

                if "# Branches" in df.columns:
                    total_branches = df["# Branches"].sum()
                    file_result["Branches"] = total_branches
                else:
                    file_result["Branches"] = "Missing column"

                if "# Junctions" in df.columns:
                    total_junctions = df["# Junctions"].sum()
                    file_result["Junctions"] = total_junctions
                else:
                    file_result["Junctions"] = "Missing column"

                if "# End-point voxels" in df.columns:
                    total_endpointvoxels = df["# End-point voxels"].sum()
                    file_result["End-point voxels"] = total_endpointvoxels
                else:
                    file_result["End-point voxels"] = "Missing column"

                if "Average Branch Length" in df.columns:
                    average_branch_length = df["Average Branch Length"].mean()
                    file_result["Average Branch Length"] = average_branch_length
                else:
                    file_result["Average Branch Length"] = "Missing column"

                results.append(file_result)

        return pd.DataFrame(results)

    except Exception as e:
        error_message = (
            f"Error occurs: {e}\n\n"
            f"Please contact [minnitijulien06@gmail.com](mailto:minnitijulien06@gmail.com) "
            f"or [Issues on GitHub](https://github.com/Jumitti/skeletonanalyzer/issues)"
        )
        st.error(error_message)


def convert_df_to_excel(df):
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Résultats')
        return output.getvalue()
    except Exception as e:
        error_message = (
            f"Error occurs: {e}\n\n"
            f"Please contact [minnitijulien06@gmail.com](mailto:minnitijulien06@gmail.com) "
            f"or [Issues on GitHub](https://github.com/Jumitti/skeletonanalyzer/issues)"
        )
        st.error(error_message)


st.set_page_config(page_title="AnalyszeSkeleton", page_icon="🦴", layout="wide")
st.title("AnalyzeSkeleton Fiji")

st.write("This software simply facilitates the processing of data obtained with the AnalyzeSkeleton tool from Fiji/ImageJ")
st.write("⚠️ This analysis is OUR way of analysing this data, and may not correspond to your needs.")
with st.expander("**Analyse**", expanded=True):
    st.write("- Branches, Junctions and End-point Voxels are sums\n\n- Average Branch Length is a mean")
st.link_button("GitHub", "")

st.divider()
col1, col2 = st.columns([1.5, 1], gap="small")
uploaded_files = col1.file_uploader("Upload .csv or .xlsx results from Fiji/ImageJ", accept_multiple_files=True,
                                    type=['csv', 'xlsx'])

with col2.expander("**Help**", expanded=False):
    st.link_button("**Fiji AnalyzeSkeleton documentation**", "https://imagej.net/plugins/analyze-skeleton/#table-of-results")
    st.image("https://imagej.net/media/plugins/analyze-skeleton/analyzeskeleton-results-table.png", "Table of results example")

if uploaded_files:
    st.divider()
    df_results = process_files(uploaded_files)
    col1, col2 = st.columns([1.5, 1], gap="small")
    col1.write("**Results**")
    col1.dataframe(df_results, hide_index=True)
    with col2.expander("**Help**", expanded=False):
        st.write("- Branches, Junctions and End-point Voxels are sums\n\n- Average Branch Length is a mean")

    excel_file = convert_df_to_excel(df_results)

    current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    col2.download_button(
        label="Download results 💾",
        data=excel_file,
        file_name=f"AnalyzeSkeleton_{current_date_time}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
