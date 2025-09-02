import os
import pandas as pd
from visualize import create_horizontal_bar_chart, create_stacked_horizontal_bar_chart, create_environmental_preferences_stacked_chart, process_multiple_choice_responses

def clean_likert_responses(df, column):
    """
    Clean and order Likert scale responses
    
    Args:
        df (pd.DataFrame): Input DataFrame
        column (str): Column name containing Likert scale responses
    
    Returns:
        pd.Series: Ordered frequency counts with proper labels
    """
    # Get value counts and sort by index
    counts = df[column].value_counts().sort_index()
    
    # Create labels based on question type
    if "concerned" in column.lower():
        labels = {
            1: "1 - Not at all concerned",
            2: "2 - Slightly concerned",
            3: "3 - Moderately concerned",
            4: "4 - Very concerned",
            5: "5 - Extremely concerned"
        }
    elif "important" in column.lower():
        labels = {
            1: "1 - Not at all important",
            2: "2 - Slightly important",
            3: "3 - Moderately important",
            4: "4 - Very important",
            5: "5 - Extremely important"
        }
    elif any(term in column.lower() for term in ["would you like", "would you prefer", "influence"]):
        labels = {
            1: "1 - Definitely not",
            2: "2 - Probably not",
            3: "3 - Maybe",
            4: "4 - Probably yes",
            5: "5 - Definitely yes"
        }
    elif "agree" in column.lower():
        labels = {
            1: "1 - Strongly disagree",
            2: "2 - Disagree",
            3: "3 - Neither agree nor disagree",
            4: "4 - Agree",
            5: "5 - Strongly agree"
        }
    else:
        labels = {str(i): f"{i}" for i in range(1, 6)}
    
    # Map the indices to proper labels
    counts.index = [labels[i] for i in counts.index]
    
    # Ensure all scale points are included (with 0 count if not present)
    full_scale = pd.Series(index=[labels[i] for i in range(1, 6)], data=[counts.get(labels[i], 0) for i in range(1, 6)])
    
    return full_scale[full_scale > 0]  # Remove zero counts

def clean_time_responses(df, column):
    """
    Clean and order time-based responses
    
    Args:
        df (pd.DataFrame): Input DataFrame
        column (str): Column name containing time responses
    
    Returns:
        pd.Series: Ordered frequency counts
    """
    # Define the order of time categories
    time_order = [
        'Less than half an hour',
        'Half - One hour',
        '1 - 2 hours',
        'More than 2 hours'
    ]
    
    # Get value counts
    counts = df[column].value_counts()
    
    # Filter out uncertain responses
    counts = counts[~counts.index.str.contains('not sure|track|measure', case=False)]
    
    # Reorder based on time_order
    ordered_counts = pd.Series(index=time_order, data=[
        counts.get(cat, 0) for cat in time_order
    ])
    
    # Remove categories with zero counts
    return ordered_counts[ordered_counts > 0]

def analyze_survey_data(excel_path, output_dir):
    """
    Analyze LLM survey data and generate visualizations
    
    Args:
        excel_path (str): Path to the Excel file containing survey data
        output_dir (str): Directory to save output visualizations
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read survey data
    df = pd.read_excel(excel_path)
    print(f"Loaded survey data with {len(df)} responses")
    
    # Define questions to analyze
    demographics = [
        {
            'column': 'Which age group do you belong to?',
            'title': 'Age Distribution',
            'output': 'demographics/age_distribution.png',
            'multiple_choice': False
        },
        {
            'column': 'Which of the following best describes your current role in your organization?',
            'title': 'Professional Groups Distribution',
            'output': 'demographics/professional_groups.png',
            'multiple_choice': False
        },
        {
            'column': 'In which business domain are you primarily working currently?',
            'title': 'Business Domain Distribution',
            'output': 'demographics/business_domain.png',
            'multiple_choice': False
        }
    ]
    
    usage_patterns = [
        {
            'column': 'What are your primary reasons for using LLM chatbots? (please select all that apply)',
            'title': 'Primary Reasons for Using LLM Chatbots',
            'output': 'usage/primary_reasons.png',
            'multiple_choice': True
        },
        {
            'column': 'What types of conversational AI services do you use? (please select all that apply)',
            'title': 'Types of Conversational AI Services Used',
            'output': 'usage/ai_services.png',
            'multiple_choice': True
        },
        {
            'column': 'How frequently do you use conversational AI tools? ',
            'title': 'Usage Frequency of Conversational AI Tools',
            'output': 'usage/usage_frequency.png',
            'multiple_choice': False
        },
        {
            'column': 'Roughly how much time do you spend actively using such tools or interacting with LLMs on a typical day?',
            'title': 'Daily Time Spent Using LLM Tools',
            'output': 'usage/daily_usage_time.png',
            'multiple_choice': False,
            'is_time_data': True
        }
    ]
    
    environmental_impact = [
        {
            'column': 'On a scale of 1–5, how concerned are you about the environmental impact of technology in general?',
            'title': 'Level of Concern About Environmental Impact of Technology',
            'output': 'environmental/concern_level.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'Do you agree that LLM chatbots should generally be optimised to reduce energy consumption?',
            'title': 'Agreement with Optimizing LLMs for Energy Efficiency',
            'output': 'environmental/energy_optimization_agreement.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'On a scale of 1–5, how important is the environmental impact of conversational AI in your decision to use any such services?',
            'title': 'Importance of Environmental Impact in Usage Decisions',
            'output': 'environmental/impact_importance.png',
            'multiple_choice': False,
            'is_likert': True
        }
    ]
    
    environmental_preferences = [
        {
            'column': 'Would you like LLM chatbots to provide an "Eco Mode" that reduces computational power for less demanding queries?',
            'title': 'Interest in Eco Mode Feature',
            'output': 'environmental/eco_mode_interest.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'Would you prefer to use an LLM chatbot that demonstrates a smaller carbon footprint, even if it is slower or less feature-rich?',
            'title': 'Preference for Eco-Friendly LLMs Despite Limitations',
            'output': 'environmental/eco_friendly_preference.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'How important is it for you to see energy consumption information related to your conversational AI usage?',
            'title': 'Importance of Energy Consumption Information',
            'output': 'environmental/energy_info_importance.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'If such usage information was provided, would it influence how you use LLM chatbots? ',
            'title': 'Potential Influence of Energy Usage Information',
            'output': 'environmental/energy_info_influence.png',
            'multiple_choice': False,
            'is_likert': True
        },
        {
            'column': 'Would you like to set limits on your LLM chatbot usage based on environmental impact? ',
            'title': 'Interest in Setting Environmental Impact Limits',
            'output': 'environmental/impact_limits_interest.png',
            'multiple_choice': False,
            'is_likert': True
        }
    ]
    
    # Process each category
    for category, questions in [
        ('Demographics', demographics), 
        ('Usage Patterns', usage_patterns),
        ('Environmental Impact', environmental_impact),
        ('Environmental Preferences', environmental_preferences)
    ]:
        print(f"\nProcessing {category}:")
        
        # Create category directory
        category_dir = os.path.dirname(os.path.join(output_dir, questions[0]['output']))
        os.makedirs(category_dir, exist_ok=True)
        
        # Process each question
        for question in questions:
            print(f"\nProcessing: {question['title']}")
            
            try:
                # Get data
                if question.get('is_time_data', False):
                    data = clean_time_responses(df, question['column'])
                elif question.get('is_likert', False):
                    data = clean_likert_responses(df, question['column'])
                elif question['multiple_choice']:
                    data = process_multiple_choice_responses(df, question['column'])
                else:
                    data = df[question['column']].value_counts()
                
                # Create visualization
                output_path = os.path.join(output_dir, question['output'])
                create_horizontal_bar_chart(data, question['title'], output_path)
                print(f"Created visualization: {output_path}")
                
                # Create stacked version for primary reasons question
                if "primary reasons" in question['title'].lower():
                    stacked_output_path = output_path.replace('.png', '_stacked.png')
                    create_stacked_horizontal_bar_chart(data, question['title'], stacked_output_path)
                    print(f"Created stacked visualization: {stacked_output_path}")
            except KeyError as e:
                print(f"Error: Column '{question['column']}' not found in the data")
                print(f"Available columns: {', '.join(df.columns)}")
    
    # Create combined environmental preferences chart (only questions with same Likert scale)
    print("\nCreating combined environmental preferences chart...")
    environmental_questions = [
        {
            'column': 'Would you like LLM chatbots to provide an "Eco Mode" that reduces computational power for less demanding queries?',
            'title': 'Support for Eco Mode Feature'
        },
        {
            'column': 'Would you prefer to use an LLM chatbot that demonstrates a smaller carbon footprint, even if it is slower or less feature-rich?',
            'title': 'Willingness to Accept Performance Trade-offs'
        },
        {
            'column': 'If such usage information was provided, would it influence how you use LLM chatbots? ',
            'title': 'Behavioral Change from Energy Transparency'
        }
    ]
    
    # Collect data for all environmental questions
    environmental_data = {}
    for question in environmental_questions:
        try:
            data = clean_likert_responses(df, question['column'])
            environmental_data[question['title']] = data
            print(f"  - {question['title']}: {sum(data.values)} responses")
        except KeyError as e:
            print(f"  - Error: Column '{question['column']}' not found")
    
    # Create the combined chart
    if environmental_data:
        combined_output_path = os.path.join(output_dir, 'environmental/environmental_preferences_combined.png')
        create_environmental_preferences_stacked_chart(
            environmental_data, 
            'Environmental Preferences Comparison', 
            combined_output_path
        )
        print(f"Created combined environmental preferences chart: {combined_output_path}")
    else:
        print("No environmental data found for combined chart")

def main():
    # Define paths
    data_path = 'data/data.xlsx'
    output_dir = 'output/plots'
    
    # Run analysis
    analyze_survey_data(data_path, output_dir)
    print("\nAnalysis complete! Check the output/plots directory for visualizations.")

if __name__ == '__main__':
    main() 