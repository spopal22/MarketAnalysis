import pandas as pd

def state_segment(data_path):

    df = pd.read_csv(data_path)#Loads the data set

    print(f"Total records: {len(df)}")
    print(f"Product categories: {df['category_name'].nunique()}")
    print(f"Unique customer segments: {df['customer_segment'].unique()}")
    print(f"Unique customer states: {df['customer_state'].nunique()}") #Gives basic output of loaded data set

    results = {}

    for category in df['category_name'].unique():
        # Filter data for this category
        category_data = df[df['category_name'] == category]
        total_category_records = len(category_data) #Iterates through each category to perform analysis

        segment_counts = category_data['customer_segment'].value_counts() #Counts how many times each unqiue value occurs in segment column
        segment_probabilities = segment_counts / total_category_records #Coverts the count into probabilities by dividing each count by total number of unqiue values in category

        state_counts = category_data['customer_state'].value_counts().head(5) #Counts occurance of each state in dataset and selects top 5
        state_percentages = (state_counts / total_category_records * 100).round(2) #Divides count by total records and multiplies by 100 to get percentage chance

        #Stores the results for the category
        results[category] = {
            'total_records': total_category_records,
            'segment_probabilities': segment_probabilities.to_dict(),
            'top5_states': [
                {'state': state, 'count': count, 'percentage': f"{percentage}%"}
                for state, count, percentage in zip(
                    state_counts.index,
                    state_counts.values,
                    state_percentages.values
                )
            ]
        }

    return results

def predict_segment_and_state(category, results):
    if category in results:
        #Find the most probable customer segement using max() with a key function
        segment_probs = results[category]['segment_probabilities'] #Accesses previously calculated segment probabilities
        best_segment = max(segment_probs, key=segment_probs.get) #Finds segment with highest probability using max() with a key function
        #key=segment_probs.get tells max() to compare the probability values and not the segment names

        best_state = results[category]['top5_states'][0]['state'] #Gives us the highest volume states

        return {
            'category': category,
            'best_segment': best_segment,
            'best_state': best_state
        }
    else:
        return {
            'category': category,
            'best_segment': None,
            'best_state': None,
            'error': 'Category not found in training data'
        }

if __name__ == "__main__":
    data_path = '2nddataset.csv'
    results = state_segment(data_path)

    #Displays the results
    print("\nCustomer Segment Probabilities by Category")
    for category, data in results.items():
        print(f"\n{category} (Total: {data['total_records']} records)")
        print("Segment Distribution:")
        for segment, probability in data['segment_probabilities'].items():
            print(f"  - {segment}: {probability:.4f} ({probability*100:.2f}%)")

    print("\nTop 5 Customer States by Category ")
    for category, data in results.items():
        print(f"\n{category}")
        print("Top States:")
        for i, state_data in enumerate(data['top5_states'], 1):
            print(f"  {i}. {state_data['state']}: {state_data['count']} orders ({state_data['percentage']})")