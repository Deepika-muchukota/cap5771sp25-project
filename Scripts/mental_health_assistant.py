import pandas as pd
import os
import time

# Global variables to store user data
user_data = {
    "rating": None,
    "duration": None,
    "symptoms": None,
    "country": None
}

current_step = 0
datasets = {}

def load_csv(filename):
    """Load and parse CSV file"""
    try:
        return pd.read_csv(filename)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def load_all_datasets():
    """Load all datasets needed for the mental health assistant"""
    print("Initializing Mental Health Assistant...")
    
    try:
        global datasets
        datasets = {
            "prevalence": load_csv("../processed_data/processed_mental_illness_prevalence.csv"),
            "dalys": load_csv("../processed_data/dalys.csv"),
            "filled_form": load_csv("../processed_data/filled_form.csv"),
            "dealt_anxiety": load_csv("../processed_data/dealt_anxiety.csv"),
            "dealing_anxiety": load_csv("../processed_data/dealing_anxiety.csv"),
            "disorders": load_csv("../processed_data/disorders.csv")
        }
        
        # Check if all datasets loaded successfully
        all_loaded = all(df is not None for df in datasets.values())
        
        if all_loaded:
            print("All available datasets loaded successfully.")
            print("Mental Health Assistant initialized successfully.")
            print("== Mental Health Assistant ==")
            print("Type 'exit' to end the conversation.")
            print()
            return True
        else:
            print("Failed to load some datasets. Please check file paths and formats.")
            return False
            
    except Exception as e:
        print(f"Error during initialization: {e}")
        return False

def get_country_data(country):
    """Get mental health data for a specific country"""
    result = {
        "prevalence": {
            "depression": 3.3,  # Default values if data not found
            "anxiety": 3.8
        }
    }
    
    # Get prevalence data for the country
    if "prevalence" in datasets and datasets["prevalence"] is not None:
        country_data = datasets["prevalence"][datasets["prevalence"]["Entity"] == country]
        if not country_data.empty:
            # Get the most recent year
            most_recent = country_data.sort_values(by="Year", ascending=False).iloc[0]
            result["prevalence"] = {
                "depression": most_recent["Major depression"],
                "bipolar": most_recent["Bipolar disorder"],
                "eating": most_recent["Eating disorders"],
                "dysthymia": most_recent["Dysthymia"],
                "schizophrenia": most_recent["Schizophrenia"],
                "anxiety": most_recent["Anxiety disorders"]
            }
    
    # Get coping strategies data
    if "dealing_anxiety" in datasets and datasets["dealing_anxiety"] is not None:
        coping_data = datasets["dealing_anxiety"][datasets["dealing_anxiety"]["Entity"] == country]
        if not coping_data.empty:
            # Get the most recent year
            most_recent = coping_data.sort_values(by="Year", ascending=False).iloc[0]
            result["coping_strategies"] = {
                "religion": most_recent["Religious/Spiritual Activities"],
                "lifestyle": most_recent["Improved Lifestyle"],
                "work": most_recent["Changed Work Situation"],
                "relationships": most_recent["Changed Relationships"],
                "social": most_recent["Talked to Friends/Family"],
                "medication": most_recent["Took Medication"],
                "outdoors": most_recent["Spent Time Outdoors"],
                "professional": most_recent["Talked to Professional"]
            }
    
    return result

def get_global_averages():
    """Calculate global averages for mental health statistics"""
    result = {"depression": 3.4, "anxiety": 3.8}  # Default values
    
    # Calculate global average for major depression
    if "prevalence" in datasets and datasets["prevalence"] is not None:
        df = datasets["prevalence"]
        if not df.empty:
            # Get the latest year
            latest_year = df["Year"].max()
            latest_data = df[df["Year"] == latest_year]
            
            # Calculate averages
            depression_values = latest_data["Major depression"].dropna()
            anxiety_values = latest_data["Anxiety disorders"].dropna()
            
            if not depression_values.empty:
                result["depression"] = depression_values.mean()
            
            if not anxiety_values.empty:
                result["anxiety"] = anxiety_values.mean()
    
    return result

def get_mental_health_resources(country):
    """Get mental health resources for a specific country"""
    # Hardcoded resources for example purposes
    resources = {
        "India": {
            "local": [
                "AASRA Suicide Prevention Helpline: 91-9820466726",
                "National Institute of Mental Health and Neurosciences (NIMHANS): www.nimhans.ac.in",
                "The Live Love Laugh Foundation: www.thelivelovelaughfoundation.org",
                "Manas Foundation: www.manasfoundation.in",
                "SCARF India (Schizophrenia Research Foundation): www.scarfindia.org",
                "iCall Psychosocial Helpline: 022-25521111",
                "Vandrevala Foundation Mental Health Helpline: 1860-2662-345"
            ],
            "global": [
                "WHO Mental Health Website: www.who.int/mental_health",
                "International Association for Suicide Prevention: www.iasp.info"
            ]
        },
        "United States": {
            "local": [
                "National Suicide Prevention Lifeline: 1-800-273-8255",
                "Crisis Text Line: Text HOME to 741741",
                "National Alliance on Mental Illness (NAMI): www.nami.org",
                "Mental Health America: www.mhanational.org"
            ],
            "global": [
                "WHO Mental Health Website: www.who.int/mental_health",
                "International Association for Suicide Prevention: www.iasp.info"
            ]
        },
        "United Kingdom": {
            "local": [
                "Samaritans: 116 123",
                "Mind: www.mind.org.uk",
                "NHS Mental Health Services: www.nhs.uk/mental-health"
            ],
            "global": [
                "WHO Mental Health Website: www.who.int/mental_health",
                "International Association for Suicide Prevention: www.iasp.info"
            ]
        },
        "Canada": {
            "local": [
                "Crisis Services Canada: 1-833-456-4566",
                "Canadian Mental Health Association: www.cmha.ca",
                "Kids Help Phone: 1-800-668-6868"
            ],
            "global": [
                "WHO Mental Health Website: www.who.int/mental_health",
                "International Association for Suicide Prevention: www.iasp.info"
            ]
        },
        "Australia": {
            "local": [
                "Lifeline Australia: 13 11 14",
                "Beyond Blue: 1300 22 4636",
                "Headspace: www.headspace.org.au"
            ],
            "global": [
                "WHO Mental Health Website: www.who.int/mental_health",
                "International Association for Suicide Prevention: www.iasp.info"
            ]
        }
    }
    
    return resources.get(country, {
        "local": ["No specific resources found for your country"],
        "global": [
            "WHO Mental Health Website: www.who.int/mental_health",
            "International Association for Suicide Prevention: www.iasp.info"
        ]
    })

def handle_rating_input(input_text):
    """Handle user input for rating their mental wellbeing"""
    global current_step, user_data
    
    try:
        rating = int(input_text)
        
        if rating < 1 or rating > 10:
            print("Chatbot: Please enter a valid number between 1 and 10.")
            return
            
        user_data["rating"] = rating
        
        if rating <= 3:
            response = "I'm sorry to hear you're not feeling well."
        elif rating <= 6:
            response = "It sounds like you're having some challenges."
        else:
            response = "I'm glad to hear you're doing relatively well."
            
        print(f"Chatbot: {response}")
        print("Chatbot: How long have you been experiencing these feelings? (days, weeks, months?)")
        
        current_step = 1
        
    except ValueError:
        print("Chatbot: Please enter a valid number between 1 and 10 to rate your mental wellbeing.")

def handle_duration_input(input_text):
    """Handle user input for duration of symptoms"""
    global current_step, user_data
    
    user_data["duration"] = input_text
    
    print("Chatbot: Thank you for sharing. Could you describe the main symptoms or feelings you've been experiencing? [For example: anxiety, low mood, trouble sleeping, irritability, worry, panic attacks, etc.]")
    
    current_step = 2

def handle_symptoms_input(input_text):
    """Handle user input for symptoms"""
    global current_step, user_data
    
    user_data["symptoms"] = input_text
    
    print("Chatbot: Thank you for sharing those details. Which country do you live in? This will help me provide statistics and coping strategies relevant to your region. [Example countries: India, United States, United Kingdom, Canada, Australia]")
    
    current_step = 3

def handle_country_input(input_text):
    """Handle user input for country"""
    global current_step, user_data
    
    country = input_text.strip()
    user_data["country"] = country
    
    # Determine likely condition based on symptoms
    symptoms = user_data["symptoms"].lower()
    
    if "low mood" in symptoms or "sadness" in symptoms or "hopeless" in symptoms:
        condition = "depression"
    elif "worry" in symptoms or "anxious" in symptoms or "panic" in symptoms:
        condition = "anxiety"
    elif "sleep" in symptoms or "insomnia" in symptoms:
        condition = "sleep issues"
    else:
        condition = "mental health challenges"
    
    # Response based on identified condition
    if condition == "depression":
        response = "Based on what you've shared, some of your experiences might be associated with depression. Would you like to learn more about depression and coping strategies? [Please respond with: yes or no]"
    elif condition == "anxiety":
        response = "Based on what you've shared, some of your experiences might be associated with anxiety. Would you like to learn more about anxiety and coping strategies? [Please respond with: yes or no]"
    else:
        response = "Based on what you've shared, would you like to learn more about common mental health challenges and coping strategies? [Please respond with: yes or no]"
    
    print(f"Chatbot: {response}")
    
    current_step = 4

def handle_learn_more_input(input_text):
    """Handle user input for learning more about mental health"""
    global current_step
    
    affirmative = "yes" in input_text.lower()
    
    if not affirmative:
        print("Chatbot: I understand. Is there something specific about mental health you'd like to know about instead?")
        return
    
    # Get country data and global averages
    country_data = get_country_data(user_data["country"])
    global_averages = get_global_averages()
    
    # Prepare information based on likely condition
    symptoms = user_data["symptoms"].lower()
    
    if "low mood" in symptoms or "sadness" in symptoms or "hopeless" in symptoms:
        # Depression info
        depression_rate = country_data["prevalence"].get("depression", 3.3)
        global_depression = global_averages["depression"]
        comparison = "lower" if depression_rate < global_depression else "higher"
        
        response = f"""Information about Depression:

Depression (major depressive disorder) causes persistent feelings of sadness and loss of interest. It affects how you feel, think, and behave and can lead to various emotional and physical problems.
In {user_data["country"]}, approximately {depression_rate:.1f}% of the population experiences depression.
This is {comparison} than the global average of {global_depression:.1f}%.

Evidence-based strategies for managing depression:

1. Psychotherapy (especially CBT and Interpersonal Therapy)
2. Medication (antidepressants) when prescribed by a healthcare provider
3. Regular physical activity, which has been shown to reduce symptoms
4. Maintaining social connections and talking about your feelings
5. Establishing routines and setting achievable goals

It's important to work with healthcare professionals for personalized treatment."""

    elif "worry" in symptoms or "anxious" in symptoms or "panic" in symptoms:
        # Anxiety info
        anxiety_rate = country_data["prevalence"].get("anxiety", 3.8)
        global_anxiety = global_averages["anxiety"]
        comparison = "lower" if anxiety_rate < global_anxiety else "higher"
        
        response = f"""Information about Anxiety:

Anxiety disorders involve persistent, excessive worry or fear about everyday situations. Anxiety can manifest as physical symptoms and interfere with daily activities.
In {user_data["country"]}, approximately {anxiety_rate:.1f}% of the population experiences anxiety disorders.
This is {comparison} than the global average of {global_anxiety:.1f}%.

Evidence-based strategies for managing anxiety:

1. Cognitive-behavioral therapy (CBT)
2. Mindfulness and meditation practices
3. Regular physical exercise
4. Breathing techniques and progressive muscle relaxation
5. Limiting caffeine and alcohol consumption
6. Medication when prescribed by a healthcare provider

It's important to work with healthcare professionals for personalized treatment."""

    else:
        # General mental health info
        response = """Information about Mental Health:

Mental health encompasses emotional, psychological, and social well-being, affecting how we think, feel, act, handle stress, relate to others, and make choices.

Common evidence-based strategies for maintaining good mental health:

1. Regular physical activity and a balanced diet
2. Adequate sleep and consistent sleep schedule
3. Social connection and supportive relationships
4. Stress management techniques like mindfulness and relaxation
5. Setting boundaries and practicing self-care
6. Seeking professional help when needed

Remember that everyone's mental health needs are different, and what works for one person may not work for another."""

    print(f"Chatbot: {response}")
    
    # Ask about resources after providing information
    time.sleep(1)
    print("\nChatbot: If you have any other questions about mental health resources or would like to discuss something specific, feel free to ask. Would you like information about professional help resources in your region? [Please respond with: yes or no]")
    
    current_step = 5

def handle_resources_input(input_text):
    """Handle user input for resources"""
    global current_step
    
    affirmative = "yes" in input_text.lower()
    
    if not affirmative:
        print("Chatbot: I understand. Feel free to ask any other questions about mental health, or type 'exit' to end our conversation.")
        current_step = 6
        return
    
    # Get resources for the country
    resources = get_mental_health_resources(user_data["country"])
    
    response = f"""Mental Health Resources:

Resources in {user_data["country"]}:
- {"\n- ".join(resources["local"])}

Global Resources:
- {"\n- ".join(resources["global"])}

Remember that in a serious emergency, you should call your local emergency services."""
    
    print(f"Chatbot: {response}")
    current_step = 6

def process_user_input(input_text):
    """Process user input based on current conversation step"""
    if input_text.lower() == "exit":
        print("\nChatbot: Thank you for using the Mental Health Assistant. Remember that this tool provides information based on global mental health data, but is not a substitute for professional care. If you're experiencing mental health difficulties, please consider speaking with a healthcare professional.")
        return False
    
    # Process input based on current step
    if current_step == 0:
        handle_rating_input(input_text)
    elif current_step == 1:
        handle_duration_input(input_text)
    elif current_step == 2:
        handle_symptoms_input(input_text)
    elif current_step == 3:
        handle_country_input(input_text)
    elif current_step == 4:
        handle_learn_more_input(input_text)
    elif current_step == 5:
        handle_resources_input(input_text)
    else:
        print("Chatbot: If you have any other questions about mental health, feel free to ask. You can type 'exit' to end our conversation.")
    
    return True

def main():
    """Main function to run the mental health assistant"""
    # Load datasets
    initialized = load_all_datasets()
    
    if not initialized:
        print("Failed to initialize Mental Health Assistant. Please check your data files and try again.")
        return
    
    # Start conversation with initial question
    print("Chatbot: Hi! I'm your Mental Health Assistant, trained on global mental health data. I'd like to understand how you're feeling. On a scale of 1-10, how would you rate your mental wellbeing today? (1 being very poor, 10 being excellent) [Please enter a number between 1-10]")
    
    # Main conversation loop
    continue_chat = True
    while continue_chat:
        user_input = input("\nYou: ").strip()
        print()  # Add a blank line after user input
        continue_chat = process_user_input(user_input)

if __name__ == "__main__":
    main()