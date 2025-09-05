import os
import pandas as pd
from visualize import create_horizontal_bar_chart, create_stacked_horizontal_bar_chart, create_environmental_preferences_stacked_chart, process_multiple_choice_responses, create_group1_stacked_bar_chart, create_group2_stacked_bar_chart, create_group3_stacked_bar_chart, create_combined_environmental_chart

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
    
    # Create Group 1 stacked bar chart (Q1 and Q4)
    print("\nCreating Group 1 stacked bar chart...")
    group1_questions = [
        {
            'column': 'On a scale of 1–5, how concerned are you about the environmental impact of technology in general?',
            'title': 'On a scale of 1–5, how concerned are you about the environmental impact of technology in general?'
        },
        {
            'column': 'On a scale of 1–5, how important is the environmental impact of conversational AI in your decision to use any such services?',
            'title': 'On a scale of 1–5, how important is the environmental impact of conversational AI in your decision to use any such services?'
        }
    ]
    
    # Collect data for Group 1 questions
    group1_data = {}
    for question in group1_questions:
        try:
            data = clean_likert_responses(df, question['column'])
            group1_data[question['title']] = data
            print(f"  - {question['title']}: {sum(data.values)} responses")
        except KeyError as e:
            print(f"  - Error: Column '{question['column']}' not found")
    
    # Create the Group 1 chart
    if group1_data:
        group1_output_path = os.path.join(output_dir, 'environmental/group1_stacked_bar_chart.png')
        create_group1_stacked_bar_chart(
            group1_data, 
            'Environmental Attitudes: Concern vs Importance', 
            group1_output_path
        )
        print(f"Created Group 1 stacked bar chart: {group1_output_path}")
    else:
        print("No Group 1 data found for stacked bar chart")

    # Create Group 2 stacked bar chart (Q2, Q5, Q6)
    print("\nCreating Group 2 stacked bar chart...")
    group2_questions = [
        {
            'column': 'Do you agree that LLM chatbots should generally be optimised to reduce energy consumption?',
            'title': 'Large Language Model chatbots should be optimised to reduce energy consumption.'
        },
        {
            'column': 'Would you like LLM chatbots to provide an "Eco Mode" that reduces computational power for less demanding queries?',
            'title': 'I would use an \'Eco Mode\' in a chatbot that consumes less energy for simple tasks.'
        },
        {
            'column': 'Would you prefer to use an LLM chatbot that demonstrates a smaller carbon footprint, even if it is slower or less feature-rich?',
            'title': 'I would prefer a chatbot with a smaller carbon footprint, even if it is slower or less feature-rich.'
        }
    ]
    
    # Collect data for Group 2 questions
    group2_data = {}
    for question in group2_questions:
        try:
            data = clean_likert_responses(df, question['column'])
            group2_data[question['title']] = data
            print(f"  - {question['title']}: {sum(data.values)} responses")
        except KeyError as e:
            print(f"  - Error: Column '{question['column']}' not found")
    
    # Create the Group 2 chart
    if group2_data:
        group2_output_path = os.path.join(output_dir, 'environmental/group2_stacked_bar_chart.png')
        create_group2_stacked_bar_chart(
            group2_data, 
            'Environmental Preferences: Agreement with Eco-Friendly Features', 
            group2_output_path
        )
        print(f"Created Group 2 stacked bar chart: {group2_output_path}")
    else:
        print("No Group 2 data found for stacked bar chart")

    # Create Group 3 stacked bar chart (Q3, Q7, Q8)
    print("\nCreating Group 3 stacked bar chart...")
    group3_questions = [
        {
            'column': 'Currently, AI companies don\'t disclose a lot of information about the energy consumption of their models. Do you agree that AI companies should be more transparent about the environmental impact of their models and products?',
            'title': 'AI companies should be more transparent about the environmental impact of their systems.'
        },
        {
            'column': 'How important is it for you to see energy consumption information related to your conversational AI usage?',
            'title': 'It is important for me to see information about the energy consumption of a chatbot.'
        },
        {
            'column': 'If such usage information was provided, would it influence how you use LLM chatbots? ',
            'title': 'Information about energy usage would influence how I use a chatbot.'
        }
    ]
    
    # Collect data for Group 3 questions
    group3_data = {}
    for question in group3_questions:
        try:
            data = clean_likert_responses(df, question['column'])
            group3_data[question['title']] = data
            print(f"  - {question['title']}: {sum(data.values)} responses")
        except KeyError as e:
            print(f"  - Error: Column '{question['column']}' not found")
    
    # Create the Group 3 chart
    if group3_data:
        group3_output_path = os.path.join(output_dir, 'environmental/group3_stacked_bar_chart.png')
        create_group3_stacked_bar_chart(
            group3_data, 
            'Environmental Transparency: Importance and Influence of Energy Information', 
            group3_output_path
        )
        print(f"Created Group 3 stacked bar chart: {group3_output_path}")
    else:
        print("No Group 3 data found for stacked bar chart")

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

    # Create combined chart with all environmental questions (shortened labels, light blue shades)
    print("\nCreating combined environmental chart with all questions...")
    all_environmental_questions = [
        {
            'column': 'On a scale of 1–5, how concerned are you about the environmental impact of technology in general?',
            'title': '(Q11) Environmental concern (technology)'
        },
        {
            'column': 'On a scale of 1–5, how important is the environmental impact of conversational AI in your decision to use any such services?',
            'title': '(Q17) Environmental importance (AI usage)'
        },
        {
            'column': 'Do you agree that LLM chatbots should generally be optimised to reduce energy consumption?',
            'title': '(Q15) Agreement with energy optimization'
        },
        {
            'column': 'Would you like LLM chatbots to provide an "Eco Mode" that reduces computational power for less demanding queries?',
            'title': '(Q18) Support for Eco Mode feature'
        },
        {
            'column': 'Would you prefer to use an LLM chatbot that demonstrates a smaller carbon footprint, even if it is slower or less feature-rich?',
            'title': '(Q19) Preference for eco-friendly chatbots'
        },
        {
            'column': 'Currently, AI companies don\'t disclose a lot of information about the energy consumption of their models. Do you agree that AI companies should be more transparent about the environmental impact of their models and products?',
            'title': '(Q16) Support for AI transparency'
        },
        {
            'column': 'How important is it for you to see energy consumption information related to your conversational AI usage?',
            'title': '(Q20) Importance of energy information'
        },
        {
            'column': 'If such usage information was provided, would it influence how you use LLM chatbots? ',
            'title': '(Q21) Behavioral influence of energy info'
        }
    ]
    
    # Collect data for all environmental questions
    all_environmental_data = {}
    for question in all_environmental_questions:
        try:
            data = clean_likert_responses(df, question['column'])
            all_environmental_data[question['title']] = data
            print(f"  - {question['title']}: {sum(data.values)} responses")
        except KeyError as e:
            print(f"  - Error: Column '{question['column']}' not found")
    
    # Create the combined chart
    if all_environmental_data:
        all_combined_output_path = os.path.join(output_dir, 'environmental/all_environmental_combined.png')
        create_combined_environmental_chart(
            all_environmental_data, 
            'Environmental Attitudes and Preferences', 
            all_combined_output_path
        )
        print(f"Created combined environmental chart: {all_combined_output_path}")
        
        # Create the new chart without question IDs and with N=77 in X-axis
        # Note: Function create_combined_environmental_chart_no_ids was removed during refactoring
        # no_ids_output_path = os.path.join(output_dir, 'environmental', 'all_environmental_combined_no_ids.png')
        # create_combined_environmental_chart_no_ids(
        #     all_environmental_data, 
        #     'Environmental Attitudes and Preferences', 
        #     no_ids_output_path
        # )
        # print(f"Created combined environmental chart (no IDs): {no_ids_output_path}")
        
        # Create separate charts by label type groups
        print("\nCreating separate charts by label type groups...")
        
        # Group 1: Concern chart (Q11)
        concern_questions = [
            {
                'column': 'On a scale of 1–5, how concerned are you about the environmental impact of technology in general?',
                'title': 'Environmental concern (technology)'
            }
        ]
        
        concern_data = {}
        for question in concern_questions:
            try:
                data = clean_likert_responses(df, question['column'])
                concern_data[question['title']] = data
                print(f"  - {question['title']}: {sum(data.values)} responses")
            except KeyError as e:
                print(f"  - Error: Column '{question['column']}' not found")
        
        if concern_data:
            concern_output_path = os.path.join(output_dir, 'environmental', 'concern_chart.png')
            # Note: Function create_concern_chart was removed during refactoring
            # create_concern_chart(concern_data, 'Environmental Concern', concern_output_path)
        
        # Group 2: Agreement chart (Q15, Q16)
        agreement_questions = [
            {
                'column': 'Do you agree that LLM chatbots should generally be optimised to reduce energy consumption?',
                'title': 'Agreement with energy optimization'
            },
            {
                'column': 'Currently, AI companies don\'t disclose a lot of information about the energy consumption of their models. Do you agree that AI companies should be more transparent about the environmental impact of their models and products?',
                'title': 'Support for AI transparency'
            }
        ]
        
        agreement_data = {}
        for question in agreement_questions:
            try:
                data = clean_likert_responses(df, question['column'])
                agreement_data[question['title']] = data
                print(f"  - {question['title']}: {sum(data.values)} responses")
            except KeyError as e:
                print(f"  - Error: Column '{question['column']}' not found")
        
        if agreement_data:
            agreement_output_path = os.path.join(output_dir, 'environmental', 'agreement_chart.png')
            # Note: Function create_agreement_chart was removed during refactoring
            # create_agreement_chart(agreement_data, 'Environmental Agreement', agreement_output_path)
        
        # Group 3: Importance chart (Q17, Q20)
        importance_questions = [
            {
                'column': 'On a scale of 1–5, how important is the environmental impact of conversational AI in your decision to use any such services?',
                'title': 'Environmental importance (AI usage)'
            },
            {
                'column': 'How important is it for you to see energy consumption information related to your conversational AI usage?',
                'title': 'Importance of energy information'
            }
        ]
        
        importance_data = {}
        for question in importance_questions:
            try:
                data = clean_likert_responses(df, question['column'])
                importance_data[question['title']] = data
                print(f"  - {question['title']}: {sum(data.values)} responses")
            except KeyError as e:
                print(f"  - Error: Column '{question['column']}' not found")
        
        if importance_data:
            importance_output_path = os.path.join(output_dir, 'environmental', 'importance_chart.png')
            # Note: Function create_importance_chart was removed during refactoring
            # create_importance_chart(importance_data, 'Environmental Importance', importance_output_path)
        
        # Group 4: Preference chart (Q18, Q19, Q21)
        preference_questions = [
            {
                'column': 'Would you like LLM chatbots to provide an "Eco Mode" that reduces computational power for less demanding queries?',
                'title': 'Support for Eco Mode feature'
            },
            {
                'column': 'Would you prefer to use an LLM chatbot that demonstrates a smaller carbon footprint, even if it is slower or less feature-rich?',
                'title': 'Preference for eco-friendly chatbots'
            },
            {
                'column': 'If such usage information was provided, would it influence how you use LLM chatbots? ',
                'title': 'Behavioral influence of energy info'
            }
        ]
        
        preference_data = {}
        for question in preference_questions:
            try:
                data = clean_likert_responses(df, question['column'])
                preference_data[question['title']] = data
                print(f"  - {question['title']}: {sum(data.values)} responses")
            except KeyError as e:
                print(f"  - Error: Column '{question['column']}' not found")
        
        if preference_data:
            preference_output_path = os.path.join(output_dir, 'environmental', 'preference_chart.png')
            # Note: Function create_preference_chart was removed during refactoring
            # create_preference_chart(preference_data, 'Environmental Preferences', preference_output_path)
        
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