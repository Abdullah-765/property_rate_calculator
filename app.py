# app.py

import streamlit as st
from calculations import *
import os
from pdf_export import generate_pdf

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔒 Protected App")
    password = st.text_input("Enter Password", type="password")

    correct_password = st.secrets["APP_PASSWORD"]

    if st.button("Login"):
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Incorrect password")

    return False


if not check_password():
    st.stop()



st.title("🏠 Property Rate Calculator")

# --------------------------
# Optional Address
# --------------------------
property_details = st.text_area("Property Address (Optional)", height=80)

# --------------------------
# Inputs (Compact Layout)
# --------------------------
st.subheader("Property Rates")

col1, col2, col3, col4 = st.columns(4)

with col1:
    area = st.number_input("Area", min_value=0, step=1, format="%d")
with col2:
    dc_rate = st.number_input("DC Rate", min_value=0, step=1, format="%d")
with col3:
    fbr_rate = st.number_input("FBR Rate", min_value=0, step=1, format="%d")
with col4:
    rebate_percentage = st.number_input("Rebate %", min_value=0, max_value=100, step=1)

is_town_tax = st.checkbox("Town Tax (Seller)")

# --------------------------
# Calculate
# --------------------------
if st.button("Calculate", type="primary"):
    st.markdown("---")

    dc_value = calculate_dc_value(area, dc_rate)
    fbr_value = calculate_fbr_value(area, fbr_rate)
    rebate_value = calculate_rebate(fbr_value, rebate_percentage)

    if rebate_value > 0:
        final_fbr_value = fbr_value - rebate_value
    else:
        final_fbr_value = fbr_value

    advance_tax, advance_tax_percent = calculate_advance_tax(final_fbr_value)
    gain_tax, gain_tax_percent = calculate_gain_tax(final_fbr_value)

    stamp_duty = calculate_stamp_duty(dc_value)
    seller_7e = calculate_seller_7e(final_fbr_value)

    st.success(f"DC Value = Rs.{dc_value:,}/-")

    if rebate_value > 0:
        st.info(f"FBR Value before rebate = Rs.{fbr_value:,}/-")
        st.info(f"Rebate Amount = Rs.{rebate_value:,}/-")
        st.success(f"FBR Value after rebate = Rs.{round(final_fbr_value):,}/-")
    else:
        st.success(f"FBR Value = Rs.{fbr_value:,}/-")

    st.success("Scanning Fee (Buyer) = Rs.1,300/-")
    st.success(f"Stamp Duty (Buyer) = Rs.{round(stamp_duty):,}/- (2%)")
    st.success(f"Advance Tax (Buyer) = Rs.{round(advance_tax):,}/- ({advance_tax_percent}%)")
    # st.success(f"Advance Tax (Buyer) = Rs.{int(advance_tax):,}/- ({advance_tax_percent}%)")
    st.success(f"Gain Tax (Seller) = Rs.{round(gain_tax):,}/- ({gain_tax_percent}%)")
    st.success(f"7E (Seller) = Rs.{round(seller_7e):,}/- (1%)")

    if is_town_tax:
        town_tax = calculate_town_tax(dc_value)
        st.success(f"Town Tax (Seller) = Rs.{town_tax:,}/-")

    # --------------------------
    # PDF Export
    # --------------------------
    buyer_expense = stamp_duty + advance_tax + 1300
    seller_expense = gain_tax + seller_7e
    if is_town_tax:
        seller_expense += town_tax 
    total_expense = buyer_expense + seller_expense

    st.success(f"Buyer Expense = Rs.{round(buyer_expense):,}/-")
    st.success(f"Seller Expense = Rs.{round(seller_expense):,}/-")
    st.info(f"Total Expense = Rs{round(total_expense):,}/-")

    pdf_data = {
    "Area": area,
    "DC Rate": f"Rs.{dc_rate:,}/-",
    "FBR Rate": f"Rs.{fbr_rate:,}/-",
    "DC Value": f"Rs.{dc_value:,}/-",
    }

# Rebate logic
    if rebate_percentage > 0:
        pdf_data["FBR Value (before rebate)"] = f"Rs.{fbr_value:,}/-"
        pdf_data["Rebate Amount"] = f"Rs.{rebate_value:,}/-"
        pdf_data["Final FBR Value After Rebate"] = f"Rs.{final_fbr_value:,}/-"
    else:
        pdf_data["FBR Value"] = f"Rs.{fbr_value:,}/-"

# Taxes
    pdf_data["__BUYER_SECTION__"] = ""
    pdf_data["Advance Tax (Buyer)"] = f"Rs.{round(advance_tax):,}/- ({advance_tax_percent}%)"
    pdf_data["Stamp Duty (Buyer)"] = f"Rs.{round(stamp_duty):,}/-"
    pdf_data["Scanning fee (Buyer)"] = "Rs.1,300"
    pdf_data["Buyer Total"] = f"Rs.{round(buyer_expense):,}/-"
    pdf_data["__SELLER_SECTION__"] = ""
    pdf_data["Gain Tax (Seller)"] = f"Rs.{round(gain_tax):,}/- ({gain_tax_percent}%)"
    pdf_data["7E (Seller)"] = f"Rs.{round(seller_7e):,}/-"

    if is_town_tax:
        pdf_data["Town Tax (Seller)"] = f"Rs.{round(town_tax):,}/-"

    pdf_data["Seller Total"] = f"Rs.{round(seller_expense):,}/-"

    # Optional address
    if property_details:
        pdf_data["Property Address"] = property_details

    pdf_file = generate_pdf(pdf_data)

    st.download_button(
        "📄 Download PDF",
        pdf_file,
        file_name="property_rate_calculation.pdf",
        mime="application/pdf",
    )
