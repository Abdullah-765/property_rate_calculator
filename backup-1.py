import streamlit as st

st.title("Property Rate Calculator")

# Select property type
property_type = st.selectbox(
    "Select Property",
    ("Flat", "Shop", "Bungalow", "Mezzanine", "Office"),
)

# # Initialize address components
# flat_no = ""
# building_no = ""
# street = ""
# phase = ""

# # Conditional inputs based on property type
# if property_type == "Flat":
#     st.subheader("Flat Details")
#     flat_no = st.text_input("Flat No.")
#     building_no = st.text_input("Building No.")
#     street = st.text_input("Street")
#     phase = st.text_input("Phase")

# elif property_type == "Shop":
#     st.subheader("Shop Details")
#     flat_no = st.text_input("Shop No.")
#     building_no = st.text_input("Building No.")
#     street = st.text_input("Street")
#     phase = st.text_input("Phase")

# elif property_type == "Bungalow":
#     st.subheader("Bungalow Details")
#     building_no = st.text_input("Bungalow No.")
#     street = st.text_input("Street")
#     phase = st.text_input("Phase")

# elif property_type == "Mezzanine":
#     st.subheader("Mezzanine Details")
#     flat_no = st.text_input("Mezzanine No.")
#     building_no = st.text_input("Building No.")
#     street = st.text_input("Street")
#     phase = st.text_input("Phase")

# Input fields for all properties
area = st.number_input("Input area", min_value=0, step=1)
dc_rate = st.number_input("Input DC Rate", min_value=0, step=1)
fbr_rate = st.number_input("Input FBR Rate", min_value=0, step=1)
rebatePercentage = st.number_input("Input Rebate %", min_value=0, max_value=100, step=1)
stampDutyPercentage = 2 / 100
advanceTax = 0
advanceTaxPercentage = 0
gainTax = 0
gainTaxPercentage = 0
seller7E = 1 / 100
isTownTax = st.checkbox("Towntax")

# Calculation happens only after clicking the button
if st.button("Calculate"):
    # DC Value
    dcValue = area * dc_rate
    st.success(f"DC Value = Rs.{dcValue:,}/-")
    # FBR Value
    fbrValue = area * fbr_rate

    # Rebate calculation
    if rebatePercentage > 0:
        rebateValue = (rebatePercentage / 100) * fbrValue
        finalFbrValue = fbrValue - rebateValue

        st.write(f"FBR Value before rebate = Rs.{fbrValue:,}/-")
        st.write(f"Rebate Amount = Rs.{rebateValue:,}/-")
        st.success(f"FBR Value after rebate = Rs{finalFbrValue:,}/-")

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

        st.success(f"Advance Tax (Buyer): Rs.{advanceTax:,}/- ({advanceTaxPercentage}%)")
        st.success(f"Gain Tax (Seller): Rs.{gainTax:,}/- ({gainTaxPercentage}%)")
        st.success(f"7E (Seller): Rs.{seller7E * finalFbrValue:,}/- (1%)")

        
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

#GAIN TAX
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
        st.success(f"Stamp Duty (buyer) = Rs.{stampDutyPercentage * dcValue:,}/- (2%)")
        st.success(f"Advance Tax (Buyer): Rs.{advanceTax:,}/- ({advanceTaxPercentage}%)")
        st.success(f"Gain Tax (Seller): Rs.{gainTax:,}/- ({gainTaxPercentage}%)")
        st.success(f"7E (Seller): Rs.{seller7E * fbrValue:,}/- (1%)")
    if isTownTax:
        townTax = (1/100) * dcValue
        st.success(f"Town Tax (Seller): Rs.{townTax}/-=")

    # Construct and display full address
    # address_parts = []
    # if flat_no:
    #     address_parts.append(f"{property_type} No. {flat_no}")
    # if property_type != "Bungalow" and building_no:
    #     address_parts.append(f"Building No. {building_no}")
    # else:
    #     address_parts.append(f"Bungalow No. {building_no}")
    # if street:
    #     address_parts.append(f"Street {street}")
    # if phase:
    #     address_parts.append(f"Phase-{phase}")

    # full_address = ", ".join(address_parts)
    # st.info(f"Property Address: {full_address}")
