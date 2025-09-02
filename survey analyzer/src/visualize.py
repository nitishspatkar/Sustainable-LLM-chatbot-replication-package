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

def create_environmental_preferences_stacked_chart(data_dict, title, output_path):
    """
    Create a stacked horizontal bar chart for environmental preference questions
    
    Args:
        data_dict (dict): Dictionary with question names as keys and data series as values
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Define the standard Likert scale labels in order
    likert_labels = [
        "1 - Definitely not",
        "2 - Probably not", 
        "3 - Maybe",
        "4 - Probably yes",
        "5 - Definitely yes"
    ]
    
    # Create a matrix to store percentages for each question and response
    questions = list(data_dict.keys())
    n_questions = len(questions)
    
    # Create percentage matrix
    percentage_matrix = []
    for question, data in data_dict.items():
        total_responses = sum(data.values)
        percentages = []
        for label in likert_labels:
            # Find matching label in data (handle slight variations)
            matching_label = None
            for data_label in data.index:
                if label.split(' - ')[0] == data_label.split(' - ')[0]:  # Match the number part
                    matching_label = data_label
                    break
            
            if matching_label and matching_label in data.index:
                percentages.append((data[matching_label] / total_responses) * 100)
            else:
                percentages.append(0)
        percentage_matrix.append(percentages)
    
    # Convert to numpy array for easier manipulation
    import numpy as np
    percentage_matrix = np.array(percentage_matrix).T  # Transpose so rows = response options, cols = questions
    
    # Create figure with maximum width to stretch chart area to absolute maximum
    fig_width = 24  # Even wider for maximum stretching
    fig_height = 18  # Much taller for longer bars
    plt.figure(figsize=(fig_width, fig_height))
    
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Define scientific color scheme for each question
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Scientific blue, orange, green
    question_colors = colors[:n_questions]
    
    # Calculate total width for each bar (sum across questions for each response)
    total_widths = np.sum(percentage_matrix, axis=1)
    
    # Find the maximum total width to scale everything to use full horizontal space
    max_total = np.max(total_widths)
    scale_factor = 100 / max_total  # Scale so the longest bar uses full width
    
    # Create bars with different lengths scaled to use full horizontal space
    for i, (question, color) in enumerate(zip(questions, question_colors)):
        bar_widths = percentage_matrix[:, i]
        
        # Scale each bar segment to use full horizontal space
        scaled_widths = bar_widths * scale_factor
        
        # Calculate left positions for each bar segment
        left_positions = np.zeros(len(likert_labels))
        for j in range(i):
            left_positions += percentage_matrix[:, j] * scale_factor
        
        plt.barh(range(len(likert_labels)), scaled_widths, 
                left=left_positions, color=color, alpha=0.85, label=question,
                height=0.6)
    
    # Customize the chart with even larger font sizes for PDF visibility
    plt.yticks(range(len(likert_labels)), likert_labels, fontsize=48)  # Extra large Y-axis labels
    plt.xticks(range(0, 101, 20), fontsize=44)  # Extra large X-axis labels with standard 100% range
    plt.xlabel('Percentage of Responses (%)', fontsize=52, labelpad=30)  # Extra large axis labels
    # Remove y-axis label to use that space for stretching
    plt.title(f'{title}\n77 responses per question', fontsize=56, pad=40)  # Extra large title
    
    # Add legend positioned below the Y-axis labels for better space utilization
    plt.legend(fontsize=36, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
              frameon=True, fancybox=True, shadow=True, 
              borderpad=1.2, columnspacing=2.5, ncol=3)
    
    # Add percentage labels on bars with clean positioning (no background boxes)
    for i, (question, color) in enumerate(zip(questions, question_colors)):
        bar_widths = percentage_matrix[:, i]
        
        # Scale each bar segment to use full horizontal space
        scaled_widths = bar_widths * scale_factor
        
        # Calculate left positions for each bar segment
        left_positions = np.zeros(len(likert_labels))
        for j in range(i):
            left_positions += percentage_matrix[:, j] * scale_factor
        
        for j, (y_pos, percentage, scaled_width) in enumerate(zip(range(len(likert_labels)), percentage_matrix[:, i], scaled_widths)):
            if percentage > 0:  # Only show label if there's a value
                x_pos = left_positions[j] + scaled_width / 2
                # Use uniform white color for all labels for consistency
                plt.text(x_pos, y_pos, f'{percentage:.1f}%', 
                        ha='center', va='center', fontsize=34, 
                        color='white', weight='bold')
    
    # Add grid for better readability
    plt.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.8)
    
    # Remove gray background and ensure clean appearance
    plt.gca().set_facecolor('white')
    plt.gcf().set_facecolor('white')
    
    # Set axis limits to make bars spread horizontally as much as possible
    plt.xlim(0, 100)  # Standard 100% scale
    plt.ylim(-0.5, len(likert_labels) - 0.5)  # Proper Y spacing to prevent overlap
    
    # Adjust subplot to stretch chart area to absolute maximum width
    plt.subplots_adjust(bottom=0.25, left=0.001, right=0.999)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=1.0, 
                facecolor='white', edgecolor='none')
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