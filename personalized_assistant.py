import streamlit as st
import urllib.request
import json
import os
import ssl

st.set_page_config(
    page_title="SFIE Beauty Sandbox"
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: 'black';
        color: 'white';
    }
    [data-testid="stHeader"] {
        display: none;
    }
    [data-testid="stToolbar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar menu
st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Choose the app mode", ["SFIE Beauty LLM", "Personalized Beauty Care"])


# Function to allow self-signed HTTPS certificates
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)


# SFIE Beauty LLM app
def sfie_beauty_llm():
    st.title("SFIE Beauty LLM")
    api_key = st.text_input("Enter your API key:", type="password")
    prompt = st.text_area("Enter your prompt here:")

    if st.button("Process"):
        if not api_key:
            st.error("Please provide an API key.")
        elif not prompt:
            st.error("Enter your prompt.")
        elif not is_psychology_related(prompt):
            st.error("Irrelevant prompt.")
        else:
            with st.spinner('Processing...'):
                response = get_response(prompt, api_key)
                st.success("Done!")
                st.write("Response:")
                st.write(response)


# Function to check if the prompt is psychology-related
def is_psychology_related(prompt):
    psychology_keywords = [
        'skincare', 'skin health', 'skin type', 'skincare routine', 'skincare products', 'moisturizer',
        'cleanser', 'toner', 'serum', 'sunscreen', 'exfoliation', 'hydration', 'acne treatment',
        'anti-aging', 'hyperpigmentation', 'sensitive skin', 'dry skin', 'oily skin', 'combination skin',
        'skin barrier', 'collagen', 'retinol', 'vitamin C', 'hyaluronic acid', 'niacinamide',
        'peptides', 'AHAs', 'BHAs', 'natural skincare', 'dermatologist', 'facial', 'skin concerns',
        'dark spots', 'redness', 'blemishes', 'eczema', 'psoriasis', 'rosacea', 'dermatitis',
        'pore size', 'skin texture', 'skin tone', 'under-eye care', 'skin detox', 'allergic reactions'
    ]
    return any(keyword.lower() in prompt.lower() for keyword in psychology_keywords)


# Function to get response from Azure-based LLM
def get_response(prompt, api_key):
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 1,
        "stream": False
    }

    body = str.encode(json.dumps(data))

    url = ''
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_json = json.loads(result)
        return result_json['choices'][0]['message']['content']
    except urllib.error.HTTPError as error:
        return f"The request failed with status code: {error.code}\n{error.read().decode('utf8', 'ignore')}"


# Personalized Beauty Care app
def personalized_beauty_care():
    st.title("Personalized Beauty Care")

    # Define the screens
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = 1

    if st.session_state.current_screen == 1:
        screen1()
    elif st.session_state.current_screen == 2:
        screen2()
    elif st.session_state.current_screen == 3:
        screen3()
    elif st.session_state.current_screen == 4:
        screen4()
    elif st.session_state.current_screen == 5:
        screen5()
    elif st.session_state.current_screen == 6:
        screen6()
    elif st.session_state.current_screen == 7:
        screen7()
    elif st.session_state.current_screen == 8:
        screen8()
    elif st.session_state.current_screen == 9:
        process_results()


def screen1():
    st.header("Get the best SFIE Beauty routine via our AI powered Skin Analysis")
    st.text("Take the skin quiz")
    st.text("Tell us your skin goals and budget (takes 2 minutes)")
    st.text("\nUpload your photos\nAdd 3 photos for your skin analysis")
    st.text("\nView your new routine\nReceive a routine in 2 minutes based on your needs and preferences")

    if st.button("Get Started"):
        st.session_state.current_screen = 2


def screen2():
    st.header("What’s your number one skin goal?")
    st.text("Select the goal that matters to you most. You can select more later.")

    goals = [
        "Reduce blemishes", "Minimise blackheads", "Minimise pores visibility",
        "Target post blemish marks", "Lighten pigmentation", "Reduce redness",
        "Reduce wrinkles", "Smooth fine lines", "Improve elasticity",
        "Enhance radiance", "Hydrate dry skin", "Smooth texture",
        "Reduce eye wrinkles", "Brighten dark circles", "Reduce under eye bags"
    ]

    st.session_state.selected_goals = st.multiselect("Choose your skin goals", goals)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 1

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 3


def screen3():
    st.header("How would you best describe your skin?")
    st.text("Ideally, this should be assessed in the morning after you wash your face.")

    skin_types = [
        "My skin feels and looks oily all over, by midday my face appears shiny",
        "I have an oily T-zone (forehead, nose & chin) and normal/dry cheeks",
        "My skin tends to feel dry/ rough and feels tight after cleansing",
        "My skin doesn't feel noticeably oily or dry"
    ]

    st.session_state.skin_type = st.radio("Choose your skin type", skin_types)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 2

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 4


def screen4():
    st.header("How often does your skin typically react to new products?")
    st.text("Consider if you have experienced a reaction (sensitivity, redness, breakout) after using a new product.")

    reactions = ["Almost always", "Often", "Sometimes", "Rarely", "Never"]

    st.session_state.reaction_frequency = st.radio("Choose your reaction frequency", reactions)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 3

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 5


def screen5():
    st.header("How would you describe your skin tone?")
    st.text(
        "The level of melanin in your skin affects different biological processes (like your response to inflammation).")

    skin_tones = ["Very fair", "Fair", "Medium", "Olive", "Brown", "Black"]

    st.session_state.skin_tone = st.radio("Choose your skin tone", skin_tones)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 4

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 6


def screen6():
    st.header("Has your skin had any of these symptoms recently?")
    st.text("Let us know if you’ve experienced any of these in the last 3-6 months.")

    symptoms = [
        "Dehydration (dry / dull / lacklustre skin)",
        "Sudden onset of redness / skin flushing",
        "Sudden onset of blemishes",
        "Flaky / scaly patches",
        "Burning / stinging / warm feeling",
        "None"
    ]

    st.session_state.skin_symptoms = st.multiselect("Choose your symptoms", symptoms)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 5

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 7


def screen7():
    st.header("Do any of the following apply?")
    st.text("Select all that may impact your skin.")

    conditions = [
        "Need pregnancy/nursing safe routine",
        "History of eczema",
        "History of psoriasis",
        "History of rosacea",
        "History of acne",
        "Currently using a facial skin prescription",
        "Currently using non-prescription retinoid",
        "None"
    ]

    st.session_state.skin_conditions = st.multiselect("Choose your skin conditions", conditions)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 6

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 8


def screen8():
    st.header("When is your birthday?")
    st.text("As we age, our skin changes. Your skincare routine should take your age into account.")

    st.session_state.birthday_day = st.number_input("Day", min_value=1, max_value=31, value=1)
    st.session_state.birthday_month = st.selectbox("Month",
                                                   ["January", "February", "March", "April", "May", "June", "July",
                                                    "August", "September", "October", "November", "December"])
    st.session_state.birthday_year = st.number_input("Year", min_value=1900, max_value=2024, value=2000)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 7

    with col2:
        if st.button("Process"):
            st.session_state.current_screen = 9


def process_results():
    st.header("Processing your results...")

    # Compile the answers from all screens
    answers = {
        "skin_goals": st.session_state.selected_goals,
        "skin_type": st.session_state.skin_type,
        "reaction_frequency": st.session_state.reaction_frequency,
        "skin_tone": st.session_state.skin_tone,
        "skin_symptoms": st.session_state.skin_symptoms,
        "skin_conditions": st.session_state.skin_conditions,
        "birthday": f"{st.session_state.birthday_day} {st.session_state.birthday_month} {st.session_state.birthday_year}"
    }

    # Generate the prompt
    prompt = f"""
    Based on the answers provided from the questionnaire, could you provide skincare product recommendations, 
    treatment alternatives, and a skincare diagnosis and routine planner for 1 month? Here are the details:
    - Skin goals: {answers['skin_goals']}
    - Skin type: {answers['skin_type']}
    - Reaction frequency: {answers['reaction_frequency']}
    - Skin tone: {answers['skin_tone']}
    - Recent skin symptoms: {answers['skin_symptoms']}
    - Skin conditions: {answers['skin_conditions']}
    - Date of birth: {answers['birthday']}
    """

    # Assume API key is already stored in the session
    api_key = st.text_input("Enter your API key:", type="password")

    if api_key:
        with st.spinner("Getting your skincare recommendations..."):
            response = get_response(prompt, api_key)
            st.success("Here are your personalized skincare recommendations!")
            st.write(response)
    else:
        st.error("API key missing. Please provide your API key in the SFIE Beauty LLM section.")


# Main app logic
if app_mode == "SFIE Beauty LLM":
    sfie_beauty_llm()
else:
    personalized_beauty_care()
