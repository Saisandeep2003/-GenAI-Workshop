import streamlit as st
import google.generativeai as genai

st.title("Investment Planner")

genai.configure(api_key=GOOGLE_API_KEY)

def generate_text_with_gemini(prompt, model="gemini-1.5-flash"):
    try:
        model = genai.GenerativeModel(model)
        
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        st.error(f"Error in generating text: {e}")
        return ""

col1, col2 = st.columns(2)
with col1:
    goal = st.selectbox('What is your primary financial goal?', 
                        ('Saving for retirement', 'Building an emergency fund', 'Buying a house', 
                         'Paying for a child\'s education', 'Taking a dream vacation'))
    income = st.number_input('What is your current income level?')
    
with col2:
    time = st.selectbox('What is your investment time horizon?', 
                        ('Short-term (Less than 5 years)', 'Medium-term (5-10 years)', 'Long-term (10+ years)'))
    debt = st.selectbox('Do you have any existing debt?', ('Yes', 'No'))

invest = st.number_input('How much investable money do I have available?')
scale = st.slider("How comfortable are you with risk?", min_value=1, max_value=10, step=1)

user_data = f""" - Primary financial goal is {goal}
                - My current income level in INR {income} Rupees
                - My investment time horizon {time}
                - Do I have existing debt? {debt}
                - How much investable money do I have available? {invest} INR
                - How comfortable are you with risk? {scale} out of 10 """

prompt = f"""
Given the following user data:

{user_data}

Based on the above details, generate an investment plan in the following text format:

# Investment Plan

## Understanding Your Situation:
- **Your primary financial goal is**: {goal}
- **Your current income level is**: INR {income} Rupees
- **Your investment time horizon is**: {time}
- **Existing debt**: {debt}
- **Investable money available**: INR {invest}
- **Comfort with risk**: {scale} out of 10

## Investment Options & Potential Allocation:
1. **Investment Option**: High-Yield Savings Account  
   **Allocation**: 50%
   
2. **Investment Option**: Liquid Funds  
   **Allocation**: 20%

3. **Investment Option**: Blue-chip Stocks  
   **Allocation**: 10%

## Important Considerations:
- Based on your goal of {goal}, it's essential to balance stability and growth.
- If you have a long-term horizon, more aggressive investments like stocks might offer higher returns.
- If you have existing debt, focus on paying off high-interest debts before investing aggressively.
- Consider the risk level associated with each investment and your comfort level with risk.

## Disclaimer:
- This plan is not a substitute for professional financial advice. It's essential to consult with a licensed financial advisor before making any investment decisions.
"""

if st.button("Generate Investment Plan"):
    with st.spinner('Creating Investment Plan...'):
        text_area_placeholder = st.empty()

        generated_plan = generate_text_with_gemini(prompt, model="gemini-1.5-flash")
        st.subheader("Investment Plan")
        st.markdown(generated_plan)
