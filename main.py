import streamlit as st

# ---------- TITLE SECTION ----------
st.markdown(
    "<h1 style='text-align: center;'>📊 Loan Approval Prediction</h1>",
    unsafe_allow_html=True
)
st.divider()

# ---------- FORM SECTION ----------
with st.form("input_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        loan_amount=st.number_input("Loan amount: ", min_value=100000, step=1, max_value=100000000, key="loan_amount")
        if st.selectbox("Education: ", options=["Not Graduate", "Graduate"], key="education")=='Graduate':
            education=1
        else:
            education=0
        residential_assets_value=st.number_input("Residential assets value: ", min_value=0, step=1, key="residential_assets_value")
        luxury_assets_value=st.number_input("Luxury assets value: ",min_value=0,max_value=100000000,step=1, key="luxury_assets_value")

    with col2:
        loan_tenure=st.number_input("Loan tenure(yr): ",min_value=1, step=1,max_value=30, key="loan_tenure")
        annual_income=st.number_input("Annual income: ",min_value=100000, step=1, max_value=50000000, key="annual_income")
        bank_asset_value=st.number_input("Bank assets value: ",min_value=0,max_value=100000000, step=1, key="bank_asset_value")
        if st.selectbox("Employment status: ", options=["Self-employed", "Salaried"], key="employment_status")=='Self-employed':
            self_employed=0
        else:
            self_employed=1


    with col3:
        cibil_score=st.number_input("CIBIL score: ", min_value=300, step=1, max_value=900, key="cibil_score")
        dependents=st.number_input("No. of dependents: ", min_value=1, step=1, max_value=10, key="dependents")
        commercial_assets_value=st.number_input("Commercial assets value: ",min_value=0,max_value=100000000, step=1, key="commercial_assets_value")

    submit = st.form_submit_button("Submit")

loan_to_income=loan_amount/annual_income
assets_to_loan=(residential_assets_value + commercial_assets_value + luxury_assets_value + bank_asset_value)/loan_amount
estimated_EMI=loan_amount/(loan_tenure*12)
EMI_isto_income=(estimated_EMI/(annual_income/12))
def categorise_cibil_score(x):
    if x>=300 and x<=579:
        return 1
    elif x>=800 and x<=900:
        return 5
    elif x>=670 and x<=739:
        return 3
    elif x>=740 and x<=799:
        return 4
    else:
        return 2
cibil_score=categorise_cibil_score(cibil_score)

# ---------- OUTPUT ----------
if submit:

    import pickle

    @st.cache_resource
    def load_model(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    model = load_model("Model.pickle")
    
    # # Preparing the input data for prediction
    
    input_data = [[dependents, education, self_employed, cibil_score,
       loan_tenure, loan_to_income, assets_to_loan, EMI_isto_income]]

    # # Making prediction
    prediction = model.predict(input_data)

    # Displaying the result
    if prediction[0] == 1:
        st.markdown("<h3 style='text-align: center; color: green;'>✅ Loan may be Approved</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='text-align: center; color: red;'>❌ Loan may be Rejected</h3>", unsafe_allow_html=True)