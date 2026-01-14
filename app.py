# app.py

import streamlit as st
from calculations import *
from pdf_export import generate_pdf

st.title("🏠 Property Rate Calculator")

# --------------------------
# Optional Address
# --------------------------
def parse_amount(value: str) -> int:
    if not value:
        return 0
    return int(value.replace(",", ""))


def currency_input(label, key, placeholder=""):
    def format_commas():
        raw = st.session_state[key]

        # Allow empty
        if not raw:
            return

        # Remove commas
        raw_no_commas = raw.replace(",", "")

        # ❌ Reject non-numeric input
        if not raw_no_commas.isdigit():
            st.warning("Only numbers are allowed")
            st.session_state[key] = ""
            return

        # ✅ Apply comma formatting
        st.session_state[key] = f"{int(raw_no_commas):,}"

    # Ensure session_state key exists
    if key not in st.session_state:
        st.session_state[key] = ""

    st.text_input(
        label,
        key=key,
        placeholder=placeholder,
        on_change=format_commas
    )

    return parse_amount(st.session_state.get(key, ""))


property_details = st.text_area("Property Address (Optional)", height=80)

# --------------------------
# Inputs (Compact Layout)
# --------------------------
st.subheader("Property Rates")
is_value = st.radio(
    "Calculation Mode",
    ["Use Rates (per unit)", "Use Official Amount"],
    horizontal=True
)

if is_value == "Use Rates (per unit)":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        area = st.number_input("Area", min_value=0, step=1, format="%d")
    with col2:
        dc_rate = currency_input("DC Rate","dc_rate", "e.g. 9,000")
    with col3:
        fbr_rate = currency_input("FBR Rate","fbr_rate", "e.g. 9,000")
    with col4:
        rebate_percentage = st.number_input("Rebate %", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
else:
    official_value = currency_input("Official Value", "official_value", "e.g. 8,000,000")


is_town_tax = st.checkbox("Town Tax (Seller)")
is_seller_7E = st.checkbox("Seller 7E (Seller)")
is_services_charges = st.checkbox("Services Charges")

if is_services_charges:
    services_charges = currency_input("Services Charges","services_charges", "e.g. 25,000")
# --------------------------
# Calculate Button
# --------------------------
if st.button("Calculate", type="primary"):
    st.markdown("---")

    # --------------------------
    # Calculate taxes for all categories
    # -------------------------
    if is_value == "Use Official Amount":
        stamp_duty = calculate_stamp_duty(official_value)
        seller_7e = calculate_seller_7e(official_value)
        town_tax = calculate_town_tax(official_value) if is_town_tax else 0
        advance_tax_all = calculate_advance_tax_all(official_value)  # returns [val, %, val, %, val, %]
        gain_tax_all = calculate_gain_tax_all(official_value)        # same format
    else:
        # --------------------------
        # Base calculations
        # --------------------------
        dc_value = calculate_dc_value(area, dc_rate)
        fbr_value = calculate_fbr_value(area, fbr_rate)
        rebate_value = calculate_rebate(fbr_value, rebate_percentage)

        final_fbr_value = fbr_value - rebate_value if rebate_value > 0 else fbr_value
        stamp_duty = calculate_stamp_duty(dc_value)
        seller_7e = calculate_seller_7e(final_fbr_value)
        town_tax = calculate_town_tax(dc_value) if is_town_tax else 0
        advance_tax_all = calculate_advance_tax_all(final_fbr_value)  # returns [val, %, val, %, val, %]
        gain_tax_all = calculate_gain_tax_all(final_fbr_value)        # same format


    # --------------------------
    # Prepare 3 pages for PDF
    # --------------------------
    pages_data = []
    categories = ["Filer", "Non-Filer", "Late Filer"]

    for i, category in enumerate(categories):
        if is_value == "Use Official Amount":
            page = {
            "Category": category,
            "Property Address": property_details,
            "Official Amount": f"Rs.{official_value:,}/-"
            }
        # Buyer section
            page["__BUYER_SECTION__"] = ""
            page["Advance Tax (Buyer)"] = f"Rs.{round(advance_tax_all[i*2]):,}/- ({advance_tax_all[i*2+1]}%)"
            page["Stamp Duty (Buyer)"] = f"Rs.{round(stamp_duty):,}/- (2%)"
            page["Scanning Fee (Buyer)"] = "Rs.1,300/-"
            buyer_total = round(stamp_duty + advance_tax_all[i*2] + 1300)
            page["Buyer Total"] = f"Rs.{buyer_total:,}/-"

            # Seller section
            page["__SELLER_SECTION__"] = ""
            page["Gain Tax (Seller)"] = f"Rs.{round(gain_tax_all[i*2]):,}/- ({gain_tax_all[i*2+1]}%)"
            
            if is_seller_7E:
                page["7E (Seller)"] = f"Rs.{round(seller_7e):,}/- (1%)"

            if is_town_tax:
                page["Town Tax (Seller)"] = f"Rs.{round(town_tax):,}/- (1%)"

            seller_7e_value = seller_7e if is_seller_7E else 0
            seller_total = round(gain_tax_all[i*2] + seller_7e_value + town_tax)
            page["Seller Total"] = f"Rs.{seller_total:,}/-"
            if is_services_charges:
                page["Services Charges"] = f"Rs.{round(services_charges):,}/-"
                page["Total Amount (incl. Services Charges)"] = f"Rs.{seller_total + buyer_total + services_charges:,}/-"
            else:
                page["Total Amount"] = f"Rs.{seller_total + buyer_total:,}/-"
            pages_data.append(page)
    
        else:
            page = {
                "Category": category,
                "Property Address": property_details,
                "Area": area,
                "DC Rate": f"Rs.{dc_rate:,}/-",
                "FBR Rate": f"Rs.{fbr_rate:,}/-",
                "DC Value": f"Rs.{dc_value:,}/-",
            }

            # Rebate logic
            if rebate_percentage > 0:
                page["FBR Value (before rebate)"] = f"Rs.{round(fbr_value):,}/-"
                page["Rebate Percentage"] = f"{rebate_percentage}%"
                page["Final FBR Value After Rebate"] = f"Rs.{round(final_fbr_value):,}/-"
            else:
                page["FBR Value"] = f"Rs.{round(final_fbr_value):,}/-"

            # Buyer section
            page["__BUYER_SECTION__"] = ""
            page["Advance Tax (Buyer)"] = f"Rs.{round(advance_tax_all[i*2]):,}/- ({advance_tax_all[i*2+1]}%)"
            page["Stamp Duty (Buyer)"] = f"Rs.{round(stamp_duty):,}/- (2%)"
            page["Scanning Fee (Buyer)"] = "Rs.1,300/-"
            buyer_total = round(stamp_duty + advance_tax_all[i*2] + 1300)
            page["Buyer Total"] = f"Rs.{buyer_total:,}/-"

            # Seller section
            page["__SELLER_SECTION__"] = ""
            page["Gain Tax (Seller)"] = f"Rs.{round(gain_tax_all[i*2]):,}/- ({gain_tax_all[i*2+1]}%)"
            
            if is_seller_7E:
                page["7E (Seller)"] = f"Rs.{round(seller_7e):,}/- (1%)"

            if is_town_tax:
                page["Town Tax (Seller)"] = f"Rs.{round(town_tax):,}/- (1%)"

            seller_7e_value = seller_7e if is_seller_7E else 0
            seller_total = round(gain_tax_all[i*2] + seller_7e_value + town_tax)
            page["Seller Total"] = f"Rs.{seller_total:,}/-"
            if is_services_charges:
                page["Services Charges"] = f"Rs.{round(services_charges):,}/-"
                page["Total Amount (incl. Services Charges)"] = f"Rs.{seller_total + buyer_total + services_charges:,}/-"
            else:
                page["Total Amount"] = f"Rs.{seller_total + buyer_total:,}/-"
            pages_data.append(page)

    # --------------------------
    # Generate PDF
    # --------------------------
    pdf_file = generate_pdf(pages_data)

    st.download_button(
        "📄 Download PDF",
        pdf_file,
        file_name="property_rate_calculation.pdf",
        mime="application/pdf",
    )
