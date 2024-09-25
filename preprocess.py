import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess_data(file_path):
    # Load the data
    df = pd.read_csv(file_path, sep='\t', header=None)
    
    # Assign column names
    df.columns = ['id', 'label', 'statement', 'subject', 'speaker', 'job_title', 'state_info', 
                  'party_affiliation', 'barely_true_counts', 'false_counts', 'half_true_counts', 
                  'mostly_true_counts', 'pants_on_fire_counts', 'context']
    
    # Encode the labels
    label_encoder = LabelEncoder()
    df['label_encoded'] = label_encoder.fit_transform(df['label'])
    
    # Create a feature for total fact-check counts
    df['total_fact_check_counts'] = (df['barely_true_counts'] + df['false_counts'] + 
                                     df['half_true_counts'] + df['mostly_true_counts'] + 
                                     df['pants_on_fire_counts'])
    
    # Create features for the proportion of each type of fact-check
    for column in ['barely_true_counts', 'false_counts', 'half_true_counts', 'mostly_true_counts', 'pants_on_fire_counts']:
        df[f'{column}_prop'] = df[column] / df['total_fact_check_counts']
    
    # Fill NaN values with 0 (in case of division by zero)
    df = df.fillna(0)
    
    return df

def split_data(df, test_size=0.2, val_size=0.2):
    # Split the data into training and temporary sets
    train_df, temp_df = train_test_split(df, test_size=(test_size+val_size), random_state=42)
    
    # Split the temporary set into validation and test sets
    val_df, test_df = train_test_split(temp_df, test_size=(test_size/(test_size+val_size)), random_state=42)
    
    return train_df, val_df, test_df

def main():
    # Load and preprocess the data
    df = load_and_preprocess_data('data/train.tsv')
    
    # Split the data
    train_df, val_df, test_df = split_data(df)
    
    # Save the processed datasets
    train_df.to_csv('data/processed_train.csv', index=False)
    val_df.to_csv('data/processed_val.csv', index=False)
    test_df.to_csv('data/processed_test.csv', index=False)
    
    print("Data preprocessing completed. Processed files saved in the 'data' directory.")

if __name__ == "__main__":
    main()