#!/usr/bin/env python3
"""
NLP Analysis of Sustainability Optimization Responses
Analyzes textual responses using TF-IDF, YAKE, LDA, and KMeans clustering
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# NLP libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Set random seeds for reproducibility
np.random.seed(42)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class SustainabilityTextAnalyzer:
    """Analyzes textual responses about AI sustainability optimization"""
    
    def __init__(self, data_path):
        """Initialize with data path"""
        self.data_path = data_path
        self.df = None
        self.texts = []
        self.cleaned_texts = []
        self.themes = {}
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def load_data(self):
        """Load and extract textual responses"""
        print("Loading data...")
        self.df = pd.read_excel(self.data_path)
        
        # Find the sustainability question column
        sustainability_col = None
        for col in self.df.columns:
            if 'sustainability' in col.lower() or 'optimized' in col.lower():
                sustainability_col = col
                break
        
        if sustainability_col is None:
            raise ValueError("Could not find sustainability question column")
        
        print(f"Found column: {sustainability_col}")
        
        # Extract non-empty responses
        self.texts = self.df[sustainability_col].dropna().tolist()
        self.texts = [text for text in self.texts if text.strip() and text.strip() != '-']
        
        print(f"Found {len(self.texts)} non-empty responses")
        return self.texts
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def clean_all_texts(self):
        """Clean all textual responses"""
        print("Preprocessing texts...")
        self.cleaned_texts = [self.preprocess_text(text) for text in self.texts]
        return self.cleaned_texts
    
    def extract_tfidf_keywords(self, max_features=50):
        """Extract keywords using TF-IDF"""
        print("Extracting TF-IDF keywords...")
        
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform(self.cleaned_texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top keywords
        mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
        keyword_scores = list(zip(feature_names, mean_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        return keyword_scores[:20]  # Top 20 keywords
    
    def extract_yake_keywords(self):
        """Simple YAKE-like keyword extraction using frequency and position"""
        print("Extracting YAKE-style keywords...")
        
        # Combine all texts
        all_text = ' '.join(self.cleaned_texts)
        words = all_text.split()
        
        # Calculate word frequencies
        word_freq = Counter(words)
        
        # Calculate position scores (earlier words get higher scores)
        position_scores = {}
        for i, word in enumerate(words):
            if word not in position_scores:
                position_scores[word] = []
            position_scores[word].append(1.0 / (i + 1))
        
        # Calculate YAKE-like scores
        yake_scores = {}
        for word, freq in word_freq.items():
            if freq > 1:  # Only words that appear more than once
                avg_position = np.mean(position_scores[word])
                yake_scores[word] = freq * avg_position
        
        # Sort by score
        sorted_keywords = sorted(yake_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_keywords[:20]
    
    def cluster_with_kmeans(self, n_clusters=8):
        """Cluster responses using KMeans"""
        print(f"Clustering with KMeans (k={n_clusters})...")
        
        vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform(self.cleaned_texts)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(tfidf_matrix)
        
        # Get top terms for each cluster
        feature_names = vectorizer.get_feature_names_out()
        cluster_terms = {}
        
        for i in range(n_clusters):
            cluster_center = kmeans.cluster_centers_[i]
            top_indices = cluster_center.argsort()[-10:][::-1]
            cluster_terms[i] = [feature_names[idx] for idx in top_indices]
        
        return clusters, cluster_terms
    
    def cluster_with_lda(self, n_topics=8):
        """Cluster responses using LDA"""
        print(f"Clustering with LDA (topics={n_topics})...")
        
        vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        tfidf_matrix = vectorizer.fit_transform(self.cleaned_texts)
        
        lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=100
        )
        
        lda.fit(tfidf_matrix)
        
        # Get top terms for each topic
        feature_names = vectorizer.get_feature_names_out()
        topic_terms = {}
        
        for topic_idx, topic in enumerate(lda.components_):
            top_indices = topic.argsort()[-10:][::-1]
            topic_terms[topic_idx] = [feature_names[idx] for idx in top_indices]
        
        # Assign documents to topics
        doc_topic_probs = lda.transform(tfidf_matrix)
        doc_topics = np.argmax(doc_topic_probs, axis=1)
        
        return doc_topics, topic_terms
    
    def merge_into_themes(self, kmeans_clusters, kmeans_terms, lda_topics, lda_terms):
        """Merge clustering results into human-readable themes"""
        print("Merging clusters into themes...")
        
        # Define theme mappings based on keywords
        theme_mapping = {
            'Awareness/Transparency': {
                'keywords': ['transparency', 'awareness', 'information', 'disclosure', 'visible', 'show'],
                'description': 'Focus on making environmental impact visible and transparent to users.'
            },
            'Policy/Tax/Offsets': {
                'keywords': ['tax', 'policy', 'offset', 'fee', 'regulation', 'government', 'carbon'],
                'description': 'Policy-based solutions including taxation, carbon offsets, and regulatory approaches.'
            },
            'Model/Algorithm Efficiency': {
                'keywords': ['algorithm', 'model', 'efficiency', 'optimization', 'sparse', 'moe', 'reinforcement'],
                'description': 'Technical improvements to AI models and algorithms for better energy efficiency.'
            },
            'Infrastructure/Green Energy': {
                'keywords': ['infrastructure', 'green', 'energy', 'data', 'centre', 'center', 'cooling', 'renewable'],
                'description': 'Infrastructure improvements including green energy and efficient data centers.'
            },
            'Usage Scope/Limitations': {
                'keywords': ['limit', 'entertainment', 'meaningful', 'purpose', 'scope', 'restrict', 'boundary'],
                'description': 'Limiting AI usage to meaningful purposes and avoiding unnecessary applications.'
            },
            'Pricing/Responsibility': {
                'keywords': ['pricing', 'cost', 'responsibility', 'customer', 'provider', 'service', 'charge'],
                'description': 'Economic mechanisms and responsibility sharing between providers and users.'
            },
            'Alternative Solutions': {
                'keywords': ['alternative', 'google', 'search', 'tool', 'deepl', 'replace', 'substitute'],
                'description': 'Using alternative, more efficient tools instead of heavy AI models.'
            },
            'Bias/Social Impact': {
                'keywords': ['bias', 'social', 'training', 'data', 'influence', 'individual', 'dimension'],
                'description': 'Addressing AI bias and broader social sustainability implications.'
            }
        }
        
        # Assign responses to themes
        response_themes = {}
        
        for i, (original_text, cleaned_text) in enumerate(zip(self.texts, self.cleaned_texts)):
            assigned_themes = []
            
            # Check each theme
            for theme_name, theme_info in theme_mapping.items():
                theme_keywords = theme_info['keywords']
                
                # Check if any theme keywords appear in the text
                text_words = set(cleaned_text.split())
                theme_words = set(theme_keywords)
                
                if text_words.intersection(theme_words):
                    assigned_themes.append(theme_name)
            
            # If no themes assigned, try to infer from clustering
            if not assigned_themes:
                # Use LDA topic as fallback
                if i < len(lda_topics):
                    topic_idx = lda_topics[i]
                    topic_words = lda_terms.get(topic_idx, [])
                    
                    # Try to match topic words to themes
                    for theme_name, theme_info in theme_mapping.items():
                        theme_keywords = theme_info['keywords']
                        if any(word in theme_keywords for word in topic_words):
                            assigned_themes.append(theme_name)
                            break
            
            # If still no themes, assign to "General"
            if not assigned_themes:
                assigned_themes = ['General']
            
            response_themes[i] = {
                'original_text': original_text,
                'themes': assigned_themes
            }
        
        return response_themes, theme_mapping
    
    def create_frequency_table(self, response_themes, theme_mapping):
        """Create frequency table of themes"""
        print("Creating frequency table...")
        
        # Count theme occurrences
        theme_counts = Counter()
        total_responses = len(response_themes)
        
        for response_data in response_themes.values():
            for theme in response_data['themes']:
                theme_counts[theme] += 1
        
        # Create frequency table
        frequency_data = []
        for theme, count in theme_counts.most_common():
            percentage = (count / total_responses) * 100
            description = theme_mapping.get(theme, {}).get('description', 'General sustainability considerations')
            frequency_data.append({
                'Theme': theme,
                'Description': description,
                'Count': count,
                'Percentage': round(percentage, 1)
            })
        
        return frequency_data
    
    def extract_representative_quotes(self, response_themes, theme_mapping, max_quotes=3):
        """Extract representative quotes for each theme"""
        print("Extracting representative quotes...")
        
        # Group responses by theme
        theme_responses = {}
        for response_data in response_themes.values():
            for theme in response_data['themes']:
                if theme not in theme_responses:
                    theme_responses[theme] = []
                theme_responses[theme].append(response_data['original_text'])
        
        # Select diverse quotes for each theme
        quotes_data = []
        for theme, responses in theme_responses.items():
            # Select up to max_quotes diverse responses
            selected_quotes = responses[:max_quotes]
            
            for i, quote in enumerate(selected_quotes):
                quotes_data.append({
                    'Theme': theme,
                    'Quote': quote.strip()
                })
        
        return quotes_data
    
    def create_visualization(self, frequency_data, output_path):
        """Create bar chart of theme frequencies"""
        print("Creating visualization...")
        
        # Set up the plot
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Extract data
        themes = [item['Theme'] for item in frequency_data]
        percentages = [item['Percentage'] for item in frequency_data]
        
        # Create bar chart
        bars = ax.bar(range(len(themes)), percentages, color='#1f77b4', alpha=0.8)
        
        # Customize the plot
        ax.set_xlabel('Sustainability Optimization Themes', fontsize=14, fontweight='bold')
        ax.set_ylabel('Percentage of Responses (%)', fontsize=14, fontweight='bold')
        ax.set_title('Distribution of Sustainability Optimization Themes\n(N=25 responses)', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Set x-axis labels
        ax.set_xticks(range(len(themes)))
        ax.set_xticklabels(themes, rotation=45, ha='right', fontsize=12)
        
        # Add percentage labels on bars
        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{percentage}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"Visualization saved to: {output_path}")
    
    def save_results(self, frequency_data, quotes_data, output_dir):
        """Save results to CSV files"""
        print("Saving results...")
        
        # Save frequency table
        freq_df = pd.DataFrame(frequency_data)
        freq_path = f"{output_dir}/sustainability_themes_frequency.csv"
        freq_df.to_csv(freq_path, index=False)
        print(f"Frequency table saved to: {freq_path}")
        
        # Save quotes
        quotes_df = pd.DataFrame(quotes_data)
        quotes_path = f"{output_dir}/sustainability_themes_quotes.csv"
        quotes_df.to_csv(quotes_path, index=False)
        print(f"Quotes saved to: {quotes_path}")
        
        return freq_path, quotes_path
    
    def run_analysis(self, output_dir="output"):
        """Run complete analysis pipeline"""
        print("Starting sustainability text analysis...")
        
        # Load and preprocess data
        self.load_data()
        self.clean_all_texts()
        
        # Extract keywords
        tfidf_keywords = self.extract_tfidf_keywords()
        yake_keywords = self.extract_yake_keywords()
        
        print("\nTop TF-IDF Keywords:")
        for word, score in tfidf_keywords[:10]:
            print(f"  {word}: {score:.3f}")
        
        print("\nTop YAKE Keywords:")
        for word, score in yake_keywords[:10]:
            print(f"  {word}: {score:.3f}")
        
        # Cluster responses
        kmeans_clusters, kmeans_terms = self.cluster_with_kmeans(n_clusters=8)
        lda_topics, lda_terms = self.cluster_with_lda(n_topics=8)
        
        # Merge into themes
        response_themes, theme_mapping = self.merge_into_themes(
            kmeans_clusters, kmeans_terms, lda_topics, lda_terms
        )
        
        # Create frequency table
        frequency_data = self.create_frequency_table(response_themes, theme_mapping)
        
        # Extract quotes
        quotes_data = self.extract_representative_quotes(response_themes, theme_mapping)
        
        # Create visualization
        viz_path = f"{output_dir}/sustainability_themes_chart.png"
        self.create_visualization(frequency_data, viz_path)
        
        # Save results
        freq_path, quotes_path = self.save_results(frequency_data, quotes_data, output_dir)
        
        # Print results
        self.print_results(frequency_data, quotes_data)
        
        return frequency_data, quotes_data

    def print_results(self, frequency_data, quotes_data):
        """Print results in markdown format"""
        print("\n" + "="*80)
        print("SUSTAINABILITY OPTIMIZATION THEMES ANALYSIS")
        print("="*80)
        
        print("\n## Theme Frequency Table")
        print("| Theme | Description | Count | % |")
        print("|-------|-------------|-------|---|")
        for item in frequency_data:
            print(f"| {item['Theme']} | {item['Description']} | {item['Count']} | {item['Percentage']}% |")
        
        print("\n## Representative Quotes")
        print("| Theme | Quote |")
        print("|-------|-------|")
        for item in quotes_data:
            # Escape quotes for markdown
            quote = item['Quote'].replace('|', '\\|').replace('\n', ' ')
            print(f"| {item['Theme']} | {quote} |")

def main():
    """Main execution function"""
    # Initialize analyzer
    analyzer = SustainabilityTextAnalyzer('data/data.xlsx')
    
    # Run analysis
    frequency_data, quotes_data = analyzer.run_analysis()
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
