// mental-health-assistant.js
const fs = require('fs');
const readline = require('readline');
const Papa = require('papaparse');  // You'll need to install this: npm install papaparse

// Initialize datasets
let datasets = {};

// Create readline interface for user input/output
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to load and parse CSV
function loadAndParseCSV(filename) {
  try {
    const fileContent = fs.readFileSync(filename, 'utf8');
    return Papa.parse(fileContent, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true
    });
  } catch (error) {
    console.error(`Error loading ${filename}:`, error);
    return null;
  }
}

// Function to load all datasets
function loadAllDatasets() {
  console.log("Initializing Mental Health Assistant...");
  
  try {
    datasets = {
      prevalence: loadAndParseCSV('processed_mental_illness_prevalence.csv'),
      dalys: loadAndParseCSV('dalys.csv'),
      filledForm: loadAndParseCSV('filled_form.csv'),
      dealtAnxiety: loadAndParseCSV('dealt_anxiety.csv'),
      dealingAnxiety: loadAndParseCSV('dealing_anxiety.csv'),
      disorders: loadAndParseCSV('disorders.csv')
    };
    
    // Check if all datasets loaded successfully
    const allLoaded = Object.values(datasets).every(dataset => dataset !== null);
    
    if (allLoaded) {
      console.log("All available datasets loaded successfully.");
      console.log("Mental Health Assistant initialized successfully.");
      console.log("== Mental Health Assistant ==");
      console.log("Type 'exit' to end the conversation.");
      console.log();
      return true;
    } else {
      console.log("Failed to load some datasets. Please check file paths and formats.");
      return false;
    }
  } catch (error) {
    console.error("Error during initialization:", error);
    return false;
  }
}

// Function to get country-specific mental health data
function getCountryData(country) {
  const result = {
    prevalence: {
      depression: 3.3,  // Default values if data not found
      anxiety: 3.8
    }
  };
  
  // Get latest prevalence data for the country
  if (datasets.prevalence && datasets.prevalence.data) {
    const countryData = datasets.prevalence.data
      .filter(row => row.Entity === country)
      .sort((a, b) => b.Year - a.Year)[0]; // Get the most recent year
    
    if (countryData) {
      result.prevalence = {
        depression: countryData['Major depression'],
        bipolar: countryData['Bipolar disorder'],
        eating: countryData['Eating disorders'],
        dysthymia: countryData['Dysthymia'],
        schizophrenia: countryData['Schizophrenia'],
        anxiety: countryData['Anxiety disorders']
      };
    }
  }
  
  // Get coping strategies data
  if (datasets.dealingAnxiety && datasets.dealingAnxiety.data) {
    const copingData = datasets.dealingAnxiety.data
      .filter(row => row.Entity === country)
      .sort((a, b) => b.Year - a.Year)[0]; // Get the most recent year
    
    if (copingData) {
      result.copingStrategies = {
        religion: copingData['Religious/Spiritual Activities'],
        lifestyle: copingData['Improved Lifestyle'],
        work: copingData['Changed Work Situation'],
        relationships: copingData['Changed Relationships'],
        social: copingData['Talked to Friends/Family'],
        medication: copingData['Took Medication'],
        outdoors: copingData['Spent Time Outdoors'],
        professional: copingData['Talked to Professional']
      };
    }
  }
  
  return result;
}

// Function to get global averages for comparison
function getGlobalAverages() {
  const result = { depression: 3.4, anxiety: 3.8 }; // Default values
  
  // Calculate global average for major depression
  if (datasets.prevalence && datasets.prevalence.data && datasets.prevalence.data.length > 0) {
    const latestYearData = datasets.prevalence.data
      .map(row => row.Year)
      .reduce((max, year) => Math.max(max, year), 0);
    
    const latestData = datasets.prevalence.data
      .filter(row => row.Year === latestYearData);
    
    if (latestData.length > 0) {
      // Calculate averages
      const depressionValues = latestData
        .map(row => row['Major depression'])
        .filter(val => val !== undefined && val !== null);
      
      const anxietyValues = latestData
        .map(row => row['Anxiety disorders'])
        .filter(val => val !== undefined && val !== null);
      
      if (depressionValues.length > 0) {
        const depressionSum = depressionValues.reduce((sum, val) => sum + val, 0);
        result.depression = depressionSum / depressionValues.length;
      }
      
      if (anxietyValues.length > 0) {
        const anxietySum = anxietyValues.reduce((sum, val) => sum + val, 0);
        result.anxiety = anxietySum / anxietyValues.length;
      }
    }
  }
  
  return result;
}

// Function to get mental health resources by country
function getMentalHealthResources(country) {
  // This would typically come from a database, but for this example we'll hardcode some resources
  const resources = {
    'India': {
      local: [
        'AASRA Suicide Prevention Helpline: 91-9820466726',
        'National Institute of Mental Health and Neurosciences (NIMHANS): www.nimhans.ac.in',
        'The Live Love Laugh Foundation: www.thelivelovelaughfoundation.org',
        'Manas Foundation: www.manasfoundation.in',
        'SCARF India (Schizophrenia Research Foundation): www.scarfindia.org',
        'iCall Psychosocial Helpline: 022-25521111',
        'Vandrevala Foundation Mental Health Helpline: 1860-2662-345'
      ],
      global: [
        'WHO Mental Health Website: www.who.int/mental_health',
        'International Association for Suicide Prevention: www.iasp.info'
      ]
    },
    'United States': {
      local: [
        'National Suicide Prevention Lifeline: 1-800-273-8255',
        'Crisis Text Line: Text HOME to 741741',
        'National Alliance on Mental Illness (NAMI): www.nami.org',
        'Mental Health America: www.mhanational.org'
      ],
      global: [
        'WHO Mental Health Website: www.who.int/mental_health',
        'International Association for Suicide Prevention: www.iasp.info'
      ]
    },
    'United Kingdom': {
      local: [
        'Samaritans: 116 123',
        'Mind: www.mind.org.uk',
        'NHS Mental Health Services: www.nhs.uk/mental-health'
      ],
      global: [
        'WHO Mental Health Website: www.who.int/mental_health',
        'International Association for Suicide Prevention: www.iasp.info'
      ]
    },
    'Canada': {
      local: [
        'Crisis Services Canada: 1-833-456-4566',
        'Canadian Mental Health Association: www.cmha.ca',
        'Kids Help Phone: 1-800-668-6868'
      ],
      global: [
        'WHO Mental Health Website: www.who.int/mental_health',
        'International Association for Suicide Prevention: www.iasp.info'
      ]
    },
    'Australia': {
      local: [
        'Lifeline Australia: 13 11 14',
        'Beyond Blue: 1300 22 4636',
        'Headspace: www.headspace.org.au'
      ],
      global: [
        'WHO Mental Health Website: www.who.int/mental_health',
        'International Association for Suicide Prevention: www.iasp.info'
      ]
    }
  };
  
  return resources[country] || { 
    local: ['No specific resources found for your country'],
    global: [
      'WHO Mental Health Website: www.who.int/mental_health',
      'International Association for Suicide Prevention: www.iasp.info'
    ]
  };
}

// Chat flow state
let currentStep = 0;
let userData = {
  rating: null,
  duration: null,
  symptoms: null,
  country: null
};

// Function to start the chatbot conversation
function startChatbot() {
  // Ask first question
  console.log("Chatbot: Hi! I'm your Mental Health Assistant, trained on global mental health data. I'd like to understand how you're feeling. On a scale of 1-10, how would you rate your mental wellbeing today? (1 being very poor, 10 being excellent) [Please enter a number between 1-10]");
  
  // Start the conversation loop
  rl.on('line', (input) => {
    if (input.toLowerCase() === 'exit') {
      console.log("Chatbot: Thank you for using the Mental Health Assistant. Remember that this tool provides information based on global mental health data, but is not a substitute for professional care. If you're experiencing mental health difficulties, please consider speaking with a healthcare professional.");
      rl.close();
      return;
    }
    
    // Process user input based on current step
    processInput(input);
  });
}

// Function to process user input based on current conversation step
function processInput(input) {
  switch (currentStep) {
    case 0: // Rating step
      handleRatingInput(input);
      break;
    case 1: // Duration step
      handleDurationInput(input);
      break;
    case 2: // Symptoms step
      handleSymptomsInput(input);
      break;
    case 3: // Country step
      handleCountryInput(input);
      break;
    case 4: // Learn more step
      handleLearnMoreInput(input);
      break;
    case 5: // Resources step
      handleResourcesInput(input);
      break;
    default:
      // Default response for any additional questions
      console.log("Chatbot: If you have any other questions about mental health, feel free to ask. You can type 'exit' to end our conversation.");
      break;
  }
}

// Step handlers
function handleRatingInput(input) {
  const rating = parseInt(input);
  
  if (isNaN(rating) || rating < 1 || rating > 10) {
    console.log("Chatbot: Please enter a valid number between 1 and 10 to rate your mental wellbeing.");
    return;
  }
  
  userData.rating = rating;
  
  let response;
  if (rating <= 3) {
    response = "I'm sorry to hear you're not feeling well.";
  } else if (rating <= 6) {
    response = "It sounds like you're having some challenges.";
  } else {
    response = "I'm glad to hear you're doing relatively well.";
  }
  
  console.log(`Chatbot: ${response}`);
  console.log("Chatbot: How long have you been experiencing these feelings? (days, weeks, months?)");
  
  currentStep = 1;
}

function handleDurationInput(input) {
  userData.duration = input;
  
  console.log("Chatbot: Thank you for sharing. Could you describe the main symptoms or feelings you've been experiencing? [For example: anxiety, low mood, trouble sleeping, irritability, worry, panic attacks, etc.]");
  
  currentStep = 2;
}

function handleSymptomsInput(input) {
  userData.symptoms = input;
  
  console.log("Chatbot: Thank you for sharing those details. Which country do you live in? This will help me provide statistics and coping strategies relevant to your region. [Example countries: India, United States, United Kingdom, Canada, Australia]");
  
  currentStep = 3;
}

function handleCountryInput(input) {
  const country = input.trim();
  userData.country = country;
  
  // Determine likely condition based on symptoms
  const symptoms = userData.symptoms.toLowerCase();
  let condition = "";
  
  if (symptoms.includes("low mood") || symptoms.includes("sadness") || symptoms.includes("hopeless")) {
    condition = "depression";
  } else if (symptoms.includes("worry") || symptoms.includes("anxious") || symptoms.includes("panic")) {
    condition = "anxiety";
  } else if (symptoms.includes("sleep") || symptoms.includes("insomnia")) {
    condition = "sleep issues";
  } else {
    condition = "mental health challenges";
  }
  
  // Response based on identified condition
  let response;
  if (condition === "depression") {
    response = `Based on what you've shared, some of your experiences might be associated with depression. Would you like to learn more about depression and coping strategies? [Please respond with: yes or no]`;
  } else if (condition === "anxiety") {
    response = `Based on what you've shared, some of your experiences might be associated with anxiety. Would you like to learn more about anxiety and coping strategies? [Please respond with: yes or no]`;
  } else {
    response = `Based on what you've shared, would you like to learn more about common mental health challenges and coping strategies? [Please respond with: yes or no]`;
  }
  
  console.log(`Chatbot: ${response}`);
  
  currentStep = 4;
}

function handleLearnMoreInput(input) {
  const affirmative = input.toLowerCase().includes("yes");
  
  if (!affirmative) {
    console.log("Chatbot: I understand. Is there something specific about mental health you'd like to know about instead?");
    return;
  }
  
  // Get country data and global averages
  const countryData = getCountryData(userData.country);
  const globalAverages = getGlobalAverages();
  
  // Prepare information based on likely condition
  const symptoms = userData.symptoms.toLowerCase();
  let response = "";
  
  if (symptoms.includes("low mood") || symptoms.includes("sadness") || symptoms.includes("hopeless")) {
    // Depression info
    response = `Information about Depression:

Depression (major depressive disorder) causes persistent feelings of sadness and loss of interest. It affects how you feel, think, and behave and can lead to various emotional and physical problems.
In ${userData.country}, approximately ${(countryData.prevalence?.depression ?? 3.3).toFixed(1)}% of the population experiences depression.
This is ${(countryData.prevalence?.depression ?? 3.3) < globalAverages.depression ? 'lower' : 'higher'} than the global average of ${globalAverages.depression.toFixed(1)}%.

Evidence-based strategies for managing depression:

1. Psychotherapy (especially CBT and Interpersonal Therapy)
2. Medication (antidepressants) when prescribed by a healthcare provider
3. Regular physical activity, which has been shown to reduce symptoms
4. Maintaining social connections and talking about your feelings
5. Establishing routines and setting achievable goals

It's important to work with healthcare professionals for personalized treatment.`;
  } else if (symptoms.includes("worry") || symptoms.includes("anxious") || symptoms.includes("panic")) {
    // Anxiety info
    response = `Information about Anxiety:

Anxiety disorders involve persistent, excessive worry or fear about everyday situations. Anxiety can manifest as physical symptoms and interfere with daily activities.
In ${userData.country}, approximately ${(countryData.prevalence?.anxiety ?? 3.8).toFixed(1)}% of the population experiences anxiety disorders.
This is ${(countryData.prevalence?.anxiety ?? 3.8) < globalAverages.anxiety ? 'lower' : 'higher'} than the global average of ${globalAverages.anxiety.toFixed(1)}%.

Evidence-based strategies for managing anxiety:

1. Cognitive-behavioral therapy (CBT)
2. Mindfulness and meditation practices
3. Regular physical exercise
4. Breathing techniques and progressive muscle relaxation
5. Limiting caffeine and alcohol consumption
6. Medication when prescribed by a healthcare provider

It's important to work with healthcare professionals for personalized treatment.`;
  } else {
    // General mental health info
    response = `Information about Mental Health:

Mental health encompasses emotional, psychological, and social well-being, affecting how we think, feel, act, handle stress, relate to others, and make choices.

Common evidence-based strategies for maintaining good mental health:

1. Regular physical activity and a balanced diet
2. Adequate sleep and consistent sleep schedule
3. Social connection and supportive relationships
4. Stress management techniques like mindfulness and relaxation
5. Setting boundaries and practicing self-care
6. Seeking professional help when needed

Remember that everyone's mental health needs are different, and what works for one person may not work for another.`;
  }
  
  console.log(`Chatbot: ${response}`);
  
  // Ask about resources after providing information
  setTimeout(() => {
    console.log("Chatbot: If you have any other questions about mental health resources or would like to discuss something specific, feel free to ask. Would you like information about professional help resources in your region? [Please respond with: yes or no]");
    currentStep = 5;
  }, 1000);
}

function handleResourcesInput(input) {
  const affirmative = input.toLowerCase().includes("yes");
  
  if (!affirmative) {
    console.log("Chatbot: I understand. Feel free to ask any other questions about mental health, or type 'exit' to end our conversation.");
    currentStep = 6;
    return;
  }
  
  // Get resources for the country
  const resources = getMentalHealthResources(userData.country);
  
  const response = `Mental Health Resources:

Resources in ${userData.country}:
- ${resources.local.join('\n- ')}

Global Resources:
- ${resources.global.join('\n- ')}

Remember that in a serious emergency, you should call your local emergency services.`;
  
  console.log(`Chatbot: ${response}`);
  currentStep = 6;
}

// Main function to run the program
function main() {
  const initialized = loadAllDatasets();
  
  if (initialized) {
    startChatbot();
  } else {
    console.log("Failed to initialize Mental Health Assistant. Please check your data files and try again.");
    rl.close();
  }
}

// Run the program
main();