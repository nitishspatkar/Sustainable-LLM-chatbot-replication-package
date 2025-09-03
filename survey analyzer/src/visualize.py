import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def create_group1_stacked_bar_chart(data_dict, title, output_path):
    """
    Create a stacked horizontal bar chart for Group 1 (Q1 and Q4) with Likert scale responses
    Similar styling to the Environmental Preferences Comparison chart
    
    Args:
        data_dict (dict): Dictionary with question titles as keys and data series as values
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Create figure with stretched dimensions (similar to reference chart)
    fig_width = 32
    fig_height = 24
    plt.figure(figsize=(fig_width, fig_height))
    
    # Define colors for each question (scientific color scheme)
    colors = ['#1f77b4', '#ff7f0e']  # Blue and orange for the two questions
    
    # Get questions and their data
    questions = list(data_dict.keys())
    question_data = list(data_dict.values())
    
    # Create y-axis labels (Likert scale values 1-5, ordered from 5 to 1)
    y_labels = ['5 - Extremely', '4 - Very', '3 - Moderately', '2 - Slightly', '1 - Not at all']
    
    # Calculate percentages for each Likert value across both questions
    likert_percentages = {}
    for likert_val in range(1, 6):
        likert_percentages[likert_val] = []
        for data in question_data:
            # Find the corresponding value in the data by looking for the numeric value
            data_index = data.index
            matching_indices = [idx for idx in data_index if idx.startswith(f"{likert_val} -")]
            
            if matching_indices:
                # Get the count for this Likert value
                count = data[matching_indices[0]]
                total = data.sum()
                percentage = (count / total * 100)
            else:
                percentage = 0
            likert_percentages[likert_val].append(percentage)
    
    # Create horizontal stacked bars
    left = np.zeros(5)  # 5 Likert scale values
    bar_height = 0.6
    
    # Plot each question as a segment
    for i, (question, color) in enumerate(zip(questions, colors)):
        values = []
        for likert_val in range(1, 6):
            values.append(likert_percentages[likert_val][i])
        
        # Create the horizontal bar segment
        bars = plt.barh(range(5), values, left=left, 
                       color=color, label=question, height=bar_height, 
                       edgecolor='white', linewidth=0.5)
        
        # Add percentage labels on bars
        for j, (bar, value) in enumerate(zip(bars, values)):
            if value > 3:  # Only show labels for segments > 3%
                plt.text(bar.get_x() + bar.get_width()/2, 
                        bar.get_y() + bar.get_height()/2, 
                        f'{value:.1f}%', 
                        ha='center', va='center', 
                        fontsize=30, fontweight='bold', color='white')
        
        left += values
    
    # Customize the chart (similar to reference chart)
    plt.xlabel('Percentage of Responses (%)', fontsize=30, fontweight='bold')
    # plt.ylabel('Response Options', fontsize=30, fontweight='bold')  # Commented out to save space
    plt.title(f'{title}\n77 responses per question', fontsize=30, fontweight='bold', pad=20)
    
    # Set y-axis labels (Likert scale, ordered from 5 to 1)
    plt.yticks(range(5), y_labels, fontsize=30)
    plt.xticks(fontsize=30)
    
    # Set x-axis limits
    plt.xlim(0, 100)
    
    # Add legend below the chart with full question text
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1, 
              fontsize=30, frameon=True, fancybox=True, shadow=True)
    
    # Stretch the chart to use maximum horizontal space, with more bottom space for full question text
    plt.subplots_adjust(left=0.001, right=0.999, bottom=0.2, top=0.95)
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Created Group 1 stacked horizontal bar chart: {output_path}")

def create_group2_stacked_bar_chart(data_dict, title, output_path):
    """
    Create a grouped horizontal bar chart for Group 2 (Q2, Q5, Q6) with Likert scale responses
    Each question gets its own set of bars, properly scaled to 100%
    
    Args:
        data_dict (dict): Dictionary with question titles as keys and data series as values
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Create figure with stretched dimensions (similar to Group 1 chart)
    fig_width = 32
    fig_height = 24
    plt.figure(figsize=(fig_width, fig_height))
    
    # Define colors for each question (scientific color scheme)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, orange, green for the three questions
    
    # Get questions and their data
    questions = list(data_dict.keys())
    question_data = list(data_dict.values())
    
    # Create y-axis labels (Likert scale values 1-5, ordered from 5 to 1)
    y_labels = ['5 - Strongly agree', '4 - Agree', '3 - Neither agree nor disagree', '2 - Disagree', '1 - Strongly disagree']
    
    # Create grouped horizontal bars - each question gets its own set of bars
    bar_height = 0.2
    bar_spacing = 0.25
    
    # For each question, create a set of bars
    for q_idx, (question, data, color) in enumerate(zip(questions, question_data, colors)):
        # Calculate percentages for this question
        total = data.sum()
        percentages = []
        
        for likert_val in range(1, 6):
            # Find the corresponding value in the data
            data_index = data.index
            matching_indices = [idx for idx in data_index if idx.startswith(f"{likert_val} -")]
            
            if matching_indices:
                count = data[matching_indices[0]]
                percentage = (count / total * 100)
            else:
                percentage = 0
            percentages.append(percentage)
        
        # Create bars for this question
        y_positions = [i + (q_idx - 1) * bar_spacing for i in range(5)]
        
        bars = plt.barh(y_positions, percentages, height=bar_height, 
                       color=color, label=question, edgecolor='white', linewidth=0.5)
        
        # Add percentage labels on bars
        for bar, percentage in zip(bars, percentages):
            if percentage > 3:  # Only show labels for segments > 3%
                plt.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2, 
                        f'{percentage:.1f}%', 
                        ha='center', va='center', 
                        fontsize=30, fontweight='bold', color='white')
    
    # Customize the chart (similar to Group 1 chart)
    plt.xlabel('Percentage of Responses (%)', fontsize=30, fontweight='bold')
    # plt.ylabel('Response Options', fontsize=30, fontweight='bold')  # Commented out to save space
    plt.title(f'{title}\n77 responses per question', fontsize=30, fontweight='bold', pad=20)
    
    # Set y-axis labels (Likert scale, ordered from 5 to 1)
    # Position labels at the center of each group
    y_tick_positions = [i for i in range(5)]
    plt.yticks(y_tick_positions, y_labels, fontsize=30)
    plt.xticks(fontsize=30)
    
    # Set x-axis limits
    plt.xlim(0, 100)
    
    # Add legend below the chart with full question text
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=1, 
              fontsize=30, frameon=True, fancybox=True, shadow=True)
    
    # Stretch the chart to use maximum horizontal space, with more bottom space for full question text
    plt.subplots_adjust(left=0.001, right=0.999, bottom=0.2, top=0.95)
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Created Group 2 grouped horizontal bar chart: {output_path}")

def create_group3_stacked_bar_chart(data_dict, title, output_path):
    """
    Create a stacked horizontal bar chart for Group 3 (Q3, Q7, Q8) with Likert scale responses
    Questions on Y-axis, each question gets one stacked bar with all Likert responses as segments
    
    Args:
        data_dict (dict): Dictionary with question titles as keys and data series as values
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Create figure with stretched dimensions (same as Group 1 and 2 charts)
    fig_width = 32
    fig_height = 24
    plt.figure(figsize=(fig_width, fig_height))
    
    # Define colors for each Likert scale value (scientific color scheme)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Blue, orange, green, red, purple
    
    # Get questions and their data
    questions = list(data_dict.keys())
    question_data = list(data_dict.values())
    
    # Create horizontal stacked bars - each question gets one bar
    left = np.zeros(len(questions))  # Number of questions
    bar_height = 0.6
    
    # Plot each Likert scale value as a segment
    for likert_val in range(1, 6):
        values = []
        for data in question_data:
            # Find the corresponding value in the data by looking for the numeric value
            data_index = data.index
            matching_indices = [idx for idx in data_index if idx.startswith(f"{likert_val} -")]
            
            if matching_indices:
                # Get the count for this Likert value
                count = data[matching_indices[0]]
                total = data.sum()
                percentage = (count / total * 100)
            else:
                percentage = 0
            values.append(percentage)
        
        # Create the horizontal bar segment
        bars = plt.barh(range(len(questions)), values, left=left, 
                       color=colors[likert_val-1], height=bar_height, 
                       edgecolor='white', linewidth=0.5)
        
        # Add percentage labels on bars
        for j, (bar, value) in enumerate(zip(bars, values)):
            if value > 3:  # Only show labels for segments > 3%
                plt.text(bar.get_x() + bar.get_width()/2, 
                        bar.get_y() + bar.get_height()/2, 
                        f'{value:.1f}%', 
                        ha='center', va='center', 
                        fontsize=30, fontweight='bold', color='white')
        
        left += values
    
    # Customize the chart
    plt.xlabel('Percentage of Responses (%)', fontsize=30, fontweight='bold')
    # plt.ylabel('Questions', fontsize=30, fontweight='bold')  # Commented out to save space
    plt.title(f'{title}\n77 responses per question', fontsize=30, fontweight='bold', pad=20)
    
    # Set y-axis labels (questions)
    plt.yticks(range(len(questions)), questions, fontsize=30)
    plt.xticks(fontsize=30)
    
    # Set x-axis limits
    plt.xlim(0, 100)
    
    # Create legend for Likert scale values
    likert_labels = ['1 - Strongly disagree', '2 - Disagree', '3 - Neither agree nor disagree', 
                     '4 - Agree', '5 - Strongly agree']
    
    # Add legend below the chart with Likert scale labels
    plt.legend(likert_labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, 
              fontsize=30, frameon=True, fancybox=True, shadow=True)
    
    # Stretch the chart to use maximum horizontal space, with more bottom space for legend
    plt.subplots_adjust(left=0.001, right=0.999, bottom=0.2, top=0.95)
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Created Group 3 stacked horizontal bar chart: {output_path}")

def create_combined_environmental_chart(data_dict, title, output_path):
    """
    Create a combined stacked horizontal bar chart for all environmental questions
    Uses light blue shades, shorter question labels, normalized Likert scales, no header
    
    Args:
        data_dict (dict): Dictionary with question titles as keys and data series as values
        title (str): Chart title
        output_path (str): Path to save the output image
    """
    # Set font to Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Create figure with stretched dimensions
    fig_width = 32
    fig_height = 24
    plt.figure(figsize=(fig_width, fig_height))
    
    # Define light blue shades for Likert scale values
    colors = ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5']  # Light to medium blue shades
    
    # Get questions and their data
    questions = list(data_dict.keys())
    question_data = list(data_dict.values())
    
    # Create horizontal stacked bars - each question gets one bar
    left = np.zeros(len(questions))  # Number of questions
    bar_height = 0.6
    
    # Plot each Likert scale value as a segment
    for likert_val in range(1, 6):
        values = []
        for data in question_data:
            # Find the corresponding value in the data by looking for the numeric value
            data_index = data.index
            matching_indices = [idx for idx in data_index if idx.startswith(f"{likert_val} -")]
            
            if matching_indices:
                # Get the count for this Likert value
                count = data[matching_indices[0]]
                total = data.sum()
                percentage = (count / total * 100)
            else:
                percentage = 0
            values.append(percentage)
        
        # Create the horizontal bar segment
        bars = plt.barh(range(len(questions)), values, left=left, 
                       color=colors[likert_val-1], height=bar_height, 
                       edgecolor='white', linewidth=0.5)
        
        # Add percentage labels on bars
        for j, (bar, value) in enumerate(zip(bars, values)):
            if value > 3:  # Only show labels for segments > 3%
                plt.text(bar.get_x() + bar.get_width()/2, 
                        bar.get_y() + bar.get_height()/2, 
                        f'{value:.1f}%', 
                        ha='center', va='center', 
                        fontsize=35, fontweight='bold', color='black')
        
        left += values
    
    # Customize the chart
    plt.xlabel('Percentage of Responses (%)', fontsize=35, fontweight='bold')
    # plt.title(title, fontsize=35, fontweight='bold', pad=20)  # Removed title
    
    # Set y-axis labels (questions)
    plt.yticks(range(len(questions)), questions, fontsize=35)
    plt.xticks(fontsize=35)
    
    # Set x-axis limits
    plt.xlim(0, 100)
    
    # Create normalized legend for Likert scale values
    likert_labels = ['1 - Low', '2 - Below Average', '3 - Average', '4 - Above Average', '5 - High']
    
    # Add legend below the chart with normalized Likert scale labels
    plt.legend(likert_labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5, 
              fontsize=35, frameon=True, fancybox=True, shadow=True)
    
    # Stretch the chart to use maximum horizontal space, with more bottom space for legend
    plt.subplots_adjust(left=0.001, right=0.999, bottom=0.2, top=0.95)
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Created combined environmental chart: {output_path}") 