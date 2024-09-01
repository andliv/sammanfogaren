import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl

# Title and instructions
st.title('Filsammanfogaren')
st.write('Välkommen till filsammanfogaren!')
st.write("Ladda upp de filer du vill sammanfoga.")

# File uploader allowing multiple Excel files
uploaded_files_xlsx = st.file_uploader("Ladda upp dina XLSX-filer", type=["xlsx"], accept_multiple_files=True)

# Initialize empty lists to store file names and dataframes
file_names = []    
dfs = []

# Check if any files are uploaded
if uploaded_files_xlsx:
    for f in uploaded_files_xlsx:
        # Add file names to list
        file_names.append(f.name)
        # Read each file into a DataFrame and add to the list
        data = pd.read_excel(f)
        dfs.append(data)
    
    # Display the uploaded file names
    st.write("Uppladdade filer:", file_names)

    # Concatenate all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Display the concatenated DataFrame
    st.write(combined_df)

    # Convert the DataFrame to an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Reset buffer position to the beginning
    output.seek(0)
    processed_data = output.getvalue()

    # Create a download button for the combined Excel file
    st.download_button(
        label="Ladda ned sammanfogade Excel-filer",
        data=processed_data,
        file_name="combined.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.write("Ladda upp Excel-filer för att sammanfoga.")
