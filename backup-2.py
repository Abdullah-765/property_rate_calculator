import streamlit as st

# ==========================
# Constants / Default Values
# ==========================
STAMP_DUTY_PERCENTAGE = 2 / 100
SELLER_7E_PERCENTAGE = 1 / 100

# ==========================
# App Title
# ==========================
st.title("🏠 Property Rate Calculator")


# ==========================
# Optional Address Details
# ==========================
propertyDetails = st.text_input("Property Address Details (Optional)")

# ==========================
# Rates Inputs (Compact Columns)
# ==========================
st.subheader("Property Rates")
col1, col2, col3, col4 = st.columns(4)

with col1:
    area = st.number_input("Area", min_value=0, step=1, format="%d")
with col2:
    dc_rate = st.number_input("DC Rate", min_value=0, step=1, format="%d")
with col3:
    fbr_rate = st.number_input("FBR Rate", min_value=0, step=1, format="%d")
with col4:
    rebatePercentage = st.number_input("Rebate %", min_value=0, max_value=100, step=1)

# Town Tax Checkbox
isTownTax = st.checkbox("Town Tax (Seller)")

# ==========================
# Calculation
# ==========================
if st.button("Calculate", type="primary"):
    st.markdown("---")
    # DC Value
    dcValue = area * dc_rate
    st.success(f"DC Value: Rs.{dcValue:,}/-")

    # FBR Value
    fbrValue = area * fbr_rate

    # Rebate
    if rebatePercentage > 0:
        rebateValue = (rebatePercentage / 100) * fbrValue
        finalFbrValue = fbrValue - rebateValue

        st.info(f"FBR Value before rebate: Rs.{fbrValue:,}/-")
        st.info(f"Rebate Amount: Rs.{rebateValue:,}/-")
        st.success(f"FBR Value after rebate: Rs.{finalFbrValue:,}/-")

        if (finalFbrValue <= 50000000):
            advanceTax = (1.5 / 100) * finalFbrValue
            advanceTaxPercentage = 1.5
        elif (finalFbrValue > 50000000 and finalFbrValue <= 100000000):
            advanceTax = (2 / 100) * finalFbrValue
            advanceTaxPercentage = 2
        else:
            advanceTax = (2.5 / 100) * finalFbrValue
            advanceTaxPercentage = 2.5
        
        if (fbrValue <= 50000000):
            gainTax = (4.5 / 100) * fbrValue
            gainTaxPercentage = 4.5
        elif (fbrValue > 50000000 and fbrValue <= 100000000):
            gainTax = (5 / 100) * fbrValue
            gainTaxPercentage = 5
        else:
            gainTax = (5.5 / 100) * fbrValue
            gainTaxPercentage = 5.5
        st.success(f"Scanning Fee (buyer) = Rs.1300")
        st.success(f"Stamp Duty (buyer) = Rs.{STAMP_DUTY_PERCENTAGE * dcValue:,}/- (2%)")
        st.success(f"Advance Tax (Buyer): Rs.{advanceTax:,}/- ({advanceTaxPercentage}%)")
        st.success(f"Gain Tax (Seller): Rs.{gainTax:,}/- ({gainTaxPercentage}%)")
        st.success(f"7E (Seller): Rs.{SELLER_7E_PERCENTAGE * finalFbrValue:,}/- (1%)")

    else:
        if (fbrValue <= 50000000):
            advanceTax = (1.5 / 100) * fbrValue
            advanceTaxPercentage = 1.5
        elif (fbrValue > 50000000 and fbrValue <= 100000000):
            advanceTax = (2 / 100) * fbrValue
            advanceTaxPercentage = 2
        else:
            advanceTax = (2.5 / 100) * fbrValue
            advanceTaxPercentage = 2.5

        if (fbrValue <= 50000000):
            gainTax = (4.5 / 100) * fbrValue
            gainTaxPercentage = 4.5
        elif (fbrValue > 50000000 and fbrValue <= 100000000):
            gainTax = (5 / 100) * fbrValue
            gainTaxPercentage = 5
        else:
            gainTax = (5.5 / 100) * fbrValue
            gainTaxPercentage = 5.5
        st.success(f"FBR Value = Rs.{fbrValue:,}/-")
        st.success(f"Scanning Fee (buyer) = Rs.1300")
        st.success(f"Stamp Duty (buyer) = Rs.{STAMP_DUTY_PERCENTAGE * dcValue:,}/- (2%)")
        st.success(f"Advance Tax (Buyer): Rs.{advanceTax:,}/- ({advanceTaxPercentage}%)")
        st.success(f"Gain Tax (Seller): Rs.{gainTax:,}/- ({gainTaxPercentage}%)")
        st.success(f"7E (Seller): Rs.{SELLER_7E_PERCENTAGE * fbrValue:,}/- (1%)")

    if isTownTax:
        townTax = (1/100) * dcValue
        st.success(f"Town Tax (Seller): Rs.{townTax:,}/-")

    if propertyDetails:
        st.subheader("🏠 Property Address")
        st.info(propertyDetails)
