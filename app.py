# app.py

import streamlit as st
from calculations import *
from pdf_export import generate_pdf
from verification import *

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "otp_value" not in st.session_state:
    st.session_state.otp_value = None
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None

# if not st.session_state.authenticated:
#     st.title("🔒 Login with OTP")

#     user = st.selectbox("Select your name", list(USERS.keys()))

#     # STEP 1: Send OTP
#     if st.button("Send OTP"):
#         email = USERS[user]
#         otp = generate_otp()  # generated ONCE
#         st.session_state.otp_value = otp
#         st.session_state.selected_user = user

#         if send_otp(email, otp):
#             st.success(f"OTP sent to {email}")
#             st.session_state.otp_sent = True
#         else:
#             st.error("Failed to send OTP")

#     # STEP 2: Verify OTP (NO regeneration here)
#     if st.session_state.otp_sent:
#         user_otp = st.text_input(
#             "Enter the OTP received in email",
#             type="password",
#             key="otp_input"
#         )

#         if st.button("Verify OTP"):
#             if user_otp.strip() == st.session_state.otp_value:
#                 st.success(f"✅ Welcome {st.session_state.selected_user}!")
#                 st.session_state.authenticated = True

#                 # cleanup
#                 st.session_state.otp_sent = False
#                 st.session_state.otp_value = None

#                 st.rerun()
#             else:
#                 st.error("❌ Incorrect OTP. Try again.")

if not st.session_state.authenticated:

    # st.markdown(
    #     """
    #     <style>
    #     .login-card {
    #         max-width: 420px;
    #         margin: auto;
    #         padding: 30px;
    #         border-radius: 14px;
    #         background-color: #ffffff;
    #         box-shadow: 0px 10px 30px rgba(0,0,0,0.08);
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

    # st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown("### 🔐 Secure Login")
    st.caption("This app is protected. Please verify your identity.")

    st.markdown("---")

    # USER SELECTION
    user = st.selectbox(
        "👤 Select your name",
        list(USERS.keys()),
        help="Choose your registered name"
    )

    # SEND OTP
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("📨 Send OTP", use_container_width=True):
            email = USERS[user]
            otp = generate_otp()
            st.session_state.otp_value = otp
            st.session_state.selected_user = user

            if send_otp(email, otp):
                st.session_state.otp_sent = True
                st.success(f"OTP sent to **{email}**")
            else:
                st.error("Failed to send OTP")

    # OTP INPUT + VERIFY
    if st.session_state.otp_sent:
        st.markdown("#### 🔑 Enter OTP")

        user_otp = st.text_input(
            "6-digit code",
            type="password",
            placeholder="••••••",
            key="otp_input"
        )

        if st.button("✅ Verify & Login", use_container_width=True):
            if user_otp.strip() == st.session_state.otp_value:
                st.success(f"Welcome **{st.session_state.selected_user}** 👋")
                st.session_state.authenticated = True

                # cleanup
                st.session_state.otp_sent = False
                st.session_state.otp_value = None

                st.rerun()
            else:
                st.error("❌ Incorrect OTP. Please try again.")

    st.markdown("</div>", unsafe_allow_html=True)



if st.session_state.authenticated:
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
        rebate_percentage = st.number_input("Rebate %", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")

    is_town_tax = st.checkbox("Town Tax (Seller)")
    is_seller_7E = st.checkbox("Seller 7E (Seller)")
    is_services_charges = st.checkbox("Services Charges")

    if is_services_charges:
        services_charges = st.number_input("Services Charges", min_value=0, format="%d")
    # --------------------------
    # Calculate Button
    # --------------------------
    if st.button("Calculate", type="primary"):
        st.markdown("---")

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

        # --------------------------
        # Calculate taxes for all categories
        # --------------------------
        advance_tax_all = calculate_advance_tax_all(final_fbr_value)  # returns [val, %, val, %, val, %]
        gain_tax_all = calculate_gain_tax_all(final_fbr_value)        # same format

        # --------------------------
        # Prepare 3 pages for PDF
        # --------------------------
        pages_data = []
        categories = ["Filer", "Non-Filer", "Late Filer"]

        for i, category in enumerate(categories):
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

            seller_total = round(gain_tax_all[i*2] + seller_7e + town_tax)
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
