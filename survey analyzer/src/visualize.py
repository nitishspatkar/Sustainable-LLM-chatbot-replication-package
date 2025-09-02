import pandas as pd
import matplotlib.pyplot as plt

def create_stacked_horizontal_bar_chart(data, title, output_path):
    """
    Create a stacked horizontal bar chart from survey data
    
    Args:
        data (pd.Series): Data series with values and their counts
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Calculate dynamic figure size based on label lengths
    max_label_length = max(len(str(label)) for label in data.index)
    
    # Adjust figure width to accommodate longest labels
    # Base width + extra space for long labels + space for value labels
    figure_width = max(20, 16 + (max_label_length * 0.3))
    figure_height = max(10, len(data) * 0.6)  # Increased height per item
    
    # Create figure with dynamic sizing
    plt.figure(figsize=(figure_width, figure_height))
    
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Sort data in ascending order (longest bar on top)
    data_sorted = data.sort_values(ascending=True)
    
    # Create categories for stacking (High, Medium, Low usage)
    categories = ['Low Usage', 'Medium Usage', 'High Usage']
    colors = ['#E8F4FD', '#87CEEB', '#4682B4']  # Light blue to dark blue
    
    # Calculate thresholds for categorization
    max_val = data_sorted.max()
    threshold1 = max_val * 0.33
    threshold2 = max_val * 0.67
    
    # Create stacked data
    stacked_data = []
    for value in data_sorted.values:
        if value <= threshold1:
            stacked_data.append([value, 0, 0])  # Low usage
        elif value <= threshold2:
            stacked_data.append([threshold1, value - threshold1, 0])  # Medium usage
        else:
            stacked_data.append([threshold1, threshold2 - threshold1, value - threshold2])  # High usage
    
    # Create horizontal stacked bar chart
    bars = plt.barh(range(len(data_sorted)), 
                    [row[0] for row in stacked_data], 
                    color=colors[0], 
                    alpha=0.8,
                    label=categories[0])
    
    plt.barh(range(len(data_sorted)), 
             [row[1] for row in stacked_data], 
             left=[row[0] for row in stacked_data], 
             color=colors[1], 
             alpha=0.8,
             label=categories[1])
    
    plt.barh(range(len(data_sorted)), 
             [row[2] for row in stacked_data], 
             left=[sum(row[:2]) for row in stacked_data], 
             color=colors[2], 
             alpha=0.8,
             label=categories[2])
    
    # Customize the chart with large fonts
    plt.yticks(range(len(data_sorted)), data_sorted.index, fontsize=40)  # Increased to 40pt
    plt.xticks(fontsize=36)  # Increased to 36pt
    
    # Add labels
    plt.xlabel('Number of Responses', fontsize=40, labelpad=15)  # Increased to 40pt
    plt.ylabel('Response Options', fontsize=40, labelpad=15)  # Increased to 40pt
    
    # Add title
    plt.title(f'{title} (Stacked View)\n{sum(data_sorted.values)} responses', fontsize=44, pad=25)  # Increased to 44pt
    
    # Add legend
    plt.legend(fontsize=32, loc='upper right')  # Increased to 32pt
    
    # Add value labels on the bars
    total_responses = sum(data_sorted.values)
    for i, (bar, value) in enumerate(zip(bars, data_sorted.values)):
        percentage = (value / total_responses) * 100
        plt.text(value + 0.5, bar.get_y() + bar.get_height()/2,
                f'{int(value)} ({percentage:.1f}%)',
                ha='left', va='center', fontsize=36)  # Increased to 36pt
    
    # Add grid for better readability
    plt.grid(True, axis='x', alpha=0.3)
    
    # Ensure no text is cut off - increase margins significantly
    plt.margins(x=0.3, y=0.1)  # Increased margins for text safety
    
    # Remove gray background
    plt.gca().set_facecolor('white')
    plt.gcf().set_facecolor('white')
    
    # Adjust layout with more padding
    plt.tight_layout(pad=2.0)  # Increased padding
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.5)  # Increased padding
    plt.close()

def clean_and_group_responses(responses):
    """
    Clean and group similar responses
    
    Args:
        responses (list): List of response strings
    
    Returns:
        list: Cleaned and grouped responses
    """
    # Responses to exclude
    exclude_responses = [
        'testing', 'not yet found', 'getting an overview'
    ]
    
    # Mapping of similar responses
    groupings = {
        'conceptualizing': ['Conceptualizing', 'Ideation', 'Get new ideas/perspective', 'Conceptualizing, Ideation'],
        'research & learning': ['Research & learning', 'Research and learning', 'Research', 'Learning'],
        'coding assistance': ['Coding assistance', 'Code assistance', 'Programming help'],
        'searching for information': ['Searching for information', 'Information search', 'Finding information'],
        'creative writing': ['Creative writing', 'Content generation', 'Creative writing/content generation'],
        'personal organization': ['Personal organization', 'Task management', 'Personal organization', 'Scheduling', 'Summarizing'],
        'translation': ['Translation', 'Data structuring', 'Translation, data structuring'],
        'entertainment': ['Entertainment', 'Casual conversation', 'Entertainment & casual conversation'],
        'improving writing': ['Improving my writing', 'Writing improvement', 'Writing enhancement']
    }
    
    cleaned = []
    for response in responses:
        # Remove any text in parentheses and clean up
        clean_response = (response.split('(')[0]  # Remove everything after '('
                         .strip()  # Remove leading/trailing whitespace
                         .strip('.,)')  # Remove trailing punctuation and parentheses
                         .strip())  # Final whitespace cleanup
        
        # Skip if response is in exclude list or empty
        if any(exclude in clean_response.lower() for exclude in exclude_responses) or not clean_response:
            continue
            
        # Check if this response belongs to any group
        grouped = False
        for main_category, variations in groupings.items():
            if any(variation.lower() in clean_response.lower() for variation in variations):
                cleaned.append(main_category.title())
                grouped = True
                break
        
        # If no group found, just clean up the response
        if not grouped:
            # Capitalize first letter of each word
            cleaned.append(clean_response.title())
    
    return cleaned

def create_horizontal_bar_chart(data, title, output_path):
    """
    Create a horizontal bar chart from survey data
    
    Args:
        data (pd.Series): Data series with values and their counts
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Calculate dynamic figure size based on label lengths
    max_label_length = max(len(str(label)) for label in data.index)
    
    # Adjust figure width to accommodate longest labels
    # Base width + extra space for long labels + space for value labels
    figure_width = max(20, 16 + (max_label_length * 0.3))
    figure_height = max(10, len(data) * 0.6)  # Increased height per item
    
    # Create figure with dynamic sizing
    plt.figure(figsize=(figure_width, figure_height))
    
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Sort data in ascending order (longest bar on top)
    data_sorted = data.sort_values(ascending=True)
    
    # Create horizontal bar chart with a more professional color
    bars = plt.barh(range(len(data_sorted)), data_sorted.values, color='#2E86C1', alpha=0.8)
    
    # Customize the chart with MUCH larger fonts for excellent PDF readability
    plt.yticks(range(len(data_sorted)), data_sorted.index, fontsize=40)  # Increased to 40pt
    plt.xticks(fontsize=36)  # Increased to 36pt
    
    # Add labels with increased font size
    plt.xlabel('Number of Responses', fontsize=40, labelpad=15)  # Increased to 40pt
    plt.ylabel('Response Options', fontsize=40, labelpad=15)  # Increased to 40pt
    
    # Add title with response count
    plt.title(f'{title}\n{sum(data_sorted.values)} responses', fontsize=44, pad=25)  # Increased to 44pt
    
    # Add value labels on the bars
    total_responses = sum(data_sorted.values)
    for bar in bars:
        width = bar.get_width()
        percentage = (width / total_responses) * 100
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                f'{int(width)} ({percentage:.1f}%)',
                ha='left', va='center', fontsize=36)  # Increased to 36pt
    
    # Add grid for better readability
    plt.grid(True, axis='x', alpha=0.3)
    
    # Ensure no text is cut off - increase margins significantly
    plt.margins(x=0.3, y=0.1)  # Increased margins for text safety
    
    # Remove gray background
    plt.gca().set_facecolor('white')
    plt.gcf().set_facecolor('white')
    
    # Adjust layout with more padding
    plt.tight_layout(pad=2.0)  # Increased padding
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.5)  # Increased padding
    plt.close()

def process_multiple_choice_responses(df, column):
    """
    Process multiple choice responses from a DataFrame column
    
    Args:
        df (pd.DataFrame): Input DataFrame
        column (str): Column name containing multiple choice responses
        
    Returns:
        pd.Series: Frequency counts of responses
    """
    # Get responses and handle NaN values
    responses = df[column].dropna()
    
    # Split multiple responses and count occurrences
    all_responses = []
    for response in responses:
        # Split by comma and clean up each response
        reasons = [r.strip() for r in str(response).split(',') if r.strip()]
        
        # If this is the primary reasons question, group similar responses
        if "primary reasons" in column.lower():
            reasons = clean_and_group_responses(reasons)
        else:
            # For other questions, just clean up the labels
            reasons = [r.split('(')[0].strip().strip('.,)').strip().title() for r in reasons]
        
        all_responses.extend(reasons)
    
    # Count frequencies and sort by count (descending)
    return pd.Series(all_responses).value_counts() 