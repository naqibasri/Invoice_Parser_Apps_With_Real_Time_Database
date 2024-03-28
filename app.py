import streamlit as st
from PIL import Image
import pandas as pd
import ast
import io
from xlsxwriter import Workbook

from utils import *
from analysis import analysis
from database import database

def parser():
    st.title("Invoice Parser")
    st.write(
        """
        Welcome to the Invoice Parser app! Upload one or more invoice images to extract relevant information.
        You will receive the parsed invoice data including the invoice number, date, total amount, and item details.
        """
    )

    st.markdown(
        """
        **Guidelines for Usage:**
        - Upload one or more invoice images (in JPG, JPEG, or PNG format).
        - Click the "Parse All Invoices" button to extract information from uploaded invoices.
        - If prompted, provide the requested information for each invoice.
        - Once parsing is complete, you can download the summary Excel file containing parsed data.
        """
    )
    
    uploaded_files = st.file_uploader("Upload Invoice Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if not uploaded_files:
        st.warning("Please upload at least one invoice image.")
        return
    
    if st.button("Parse All Invoices"):
        invoices_data = []
        line_items = pd.DataFrame()
        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file)
                
                st.write(f"**Parsing invoice {uploaded_file.name}...** This may take a moment.")
                input_prompt = """
                    You are an invoice parser.
                    You will receive input images as invoices and
                    you need to provide the value based on the input invoice.
                """
                question = {'InvoiceNum': "What is the invoice number? Please provide the value only.",
                            'InvoiceDate': "What is the invoice date? Please provide the value only in format DD/MM/YYYY.",
                            'InvoiceItem': 'Please provide a dict of list of the items name, quantity, and price of each of the items listed in the invoice. Please give in the format {"name": ["Rubber","Pencil","Book",...],"quantity": [1,3,5,...],"price": [270.0,130.0,80.0,...]}. Provide the dict only without any further text.',
                            'InvoiceDiscount': "Can you provide the amount of discount in the invoice if any? If not available, please return 0.",
                            'InvoiceTaxes': "Can you provide the amount of taxes in the invoice if any? If not available, please return 0.",
                            'InvoiceTotal': "What is the final amount of the invoice after discount and taxes? Please provide the value only."}
                responses = []
                image_data = input_image_setup(uploaded_file)
                for info in question:
                    response = get_gemini_response(input_prompt, image_data, question[info])
                    responses.append(response)
                
                invoices_data.append({
                    "File Name": uploaded_file.name,
                    "Invoice Number": responses[0],
                    "Invoice Date": responses[1],
                    "Invoice Total": responses[5]
                })
                
                if responses[2]:
                    items = pd.DataFrame(ast.literal_eval(responses[2]))
                    line_items = pd.concat([line_items,items])
                
                st.success(f"**Invoice {uploaded_file.name} parsed successfully!**")
            except Exception as e:
                st.error(f"Error processing invoice {uploaded_file.name}: {e}")
    
        if invoices_data:
            df_list = pd.DataFrame(invoices_data)
            st.write("**List of Parsed Invoices:**")
            st.table(df_list)

            if len(line_items) > 0:
                st.write("**List of Line Items:**")
                st.table(line_items)

            excel_file_obj = io.BytesIO()
            with pd.ExcelWriter(excel_file_obj, engine='xlsxwriter') as writer:
                df_list.to_excel(writer, sheet_name='Invoices', index=False)
                if len(line_items) > 0:
                    line_items.to_excel(writer, sheet_name='Line Items', index=False)
                
                # Enhance Excel file styling
                workbook = writer.book
                worksheet1 = writer.sheets['Invoices']
                worksheet2 = writer.sheets['Line Items']
                
                # Add header formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',  # Light green background color
                    'border': 1
                })

                for col_num, value in enumerate(df_list.columns.values):
                    worksheet1.write(0, col_num, value, header_format)

                for col_num, value in enumerate(line_items.columns.values):
                    worksheet2.write(0, col_num, value, header_format)

                # Adjust column widths
                for i, col in enumerate(df_list.columns):
                    max_len = df_list[col].astype(str).str.len().max()
                    max_len = max_len if max_len < 50 else 50
                    worksheet1.set_column(i, i, max_len + 2)

                for i, col in enumerate(line_items.columns):
                    max_len = line_items[col].astype(str).str.len().max()
                    max_len = max_len if max_len < 50 else 50
                    worksheet2.set_column(i, i, max_len + 2)
                
            excel_file_obj.seek(0)
            st.download_button(
                label="Download Summary Excel",
                data=excel_file_obj,
                file_name="invoice_summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def main():
    pages = {
        "Parser": parser,
        "Database": database,
        "Analysis": analysis
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
