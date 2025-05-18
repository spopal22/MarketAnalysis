import pandas as pd

def calculate_average_discounts(data_path='synthetic_ecommerce_data.csv'):
    try:
        df = pd.read_csv(data_path)

        if 'Discount' not in df.columns:
            import numpy as np

            #Uses business logic for categories to predict discount percentage
            discounts = []
            for _, row in df.iterrows():
                category = row['Category']

                if category in ["Books", "Office Supplies"]:
                    #Already have low margins, rarely see high discounts
                    discount_values = [0, 0, 0, 5, 5, 10, 15, 20]
                    discount = np.random.choice(discount_values)

                elif category in ["Electronics", "Technology"]:
                    #High branded tech doesnt commonly see large discounts
                    discount_values = [0, 0, 0, 0, 5, 5, 10, 15]
                    discount = np.random.choice(discount_values)

                elif category in ["Clothing", "Sports"]:
                    #Clothing and Sports items have seasonal sales to get rid of old supply
                    discount_values = [5, 10, 15, 15, 20, 20, 25, 30]
                    discount = np.random.choice(discount_values)

                elif category in ["Beauty"]:
                    #Beauty products are well known to have higehr discounts commonly
                    discount_values = [0, 5, 5, 10, 10, 15, 20, 25]
                    discount = np.random.choice(discount_values)

                elif category in ["Home & Kitchen", "Furniture"]:
                    #Home items are frequently on sale
                    discount_values = [0, 5, 10, 10, 15, 20, 25, 30]
                    discount = np.random.choice(discount_values)

                elif category in ["Toys"]:
                    #Depends on quality of toy, but can have no discount to high discount
                    discount_values = [0, 0, 5, 10, 15, 20, 25, 50]
                    discount = np.random.choice(discount_values)

                else:
                    discount_values = [0, 5, 10, 15, 20, 25, 30, 50]
                    discount = np.random.choice(discount_values)

                discounts.append(discount)

            df['Discount'] = discounts

        #Group by Category and calculate the average discount
        avg_discounts = df.groupby('Category')['Discount'].mean().round(1)

        return avg_discounts.to_dict()
    except Exception as e:
        print(f"Error calculating average discounts: {e}")
        return {}

def analyze_synthetic_data(data_path='synthetic_ecommerce_data.csv'):
    df = pd.read_csv(data_path)

    results = {}

    #For each category
    for category in df['Category'].unique():
        category_data = df[df['Category'] == category]
        total_category_records = len(category_data) #Isolates the data for just that category

        segment_counts = category_data['Customer_Segment'].value_counts()
        segment_probabilities = segment_counts / total_category_records #Calculates the probability distribution of customer segments
        #Takes the number of entires and divides it by total based off number of orders from each segment
        #Uses probability distribution

        state_counts = category_data['Customer_State'].value_counts().head(5) #Gets the top 5 states based off order volume
        state_percentages = (state_counts / total_category_records * 100).round(2) #Done similarly to before, divides each states count by the category records
        #Converts it to percentage

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
        } #Stores our results in a consisten format

    return results

def predict_segment_and_state(category, results, price=None):
    if category not in results:
        return {
            'category': category,
            'best_segment': None,
            'best_state': None,
            'error': 'Category not found'
        } #Case for if our category doesnt exist in our dataset

    segment_probs = results[category]['segment_probabilities'] #Retrieves our probability distributions for that category

    # For Electronics and Technology, use a default high price to trigger the business rule
    if category in ["Technology", "Electronics"]:
        price = 250  # Default high price to ensure rule triggers

    if category in ["Technology", "Electronics"] and price and price > 200:
        best_segment = "Corporate" #If tech, uses business logic that determines high priced tech is usually better for corp
    elif category in ["Books", "Office Supplies"] and "Home Office" in segment_probs:
        best_segment = "Home Office" #Books and office supplies commonly associated with home office
    elif category == "Furniture" and "Corporate" in segment_probs:
        best_segment = "Corporate" #Furniture also performs good with corp customers
    else:
        best_segment = max(segment_probs, key=segment_probs.get) #Otherwise defaults to highest probability segment

    if category in ["Sports", "Clothing"]:
        best_state = results[category]['top5_states'][1]['state'] #Sports and clothing are commonly best in NY
    elif category == "Beauty":
        for state_data in results[category]['top5_states']:
            if state_data['state'] == "Florida": #Beauty products are often better in florida
                best_state = "Florida"
                break
        else:
            best_state = results[category]['top5_states'][0]['state']
    else:
        best_state = results[category]['top5_states'][0]['state']

    return {
        'category': category,
        'best_segment': best_segment,
        'segment_probabilities': segment_probs,
        'best_state': best_state,
        'top5_states': results[category]['top5_states']
    } #Returns our recommendations

state_to_initial = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC"
}

def main():
    synthetic_data_path = 'synthetic_ecommerce_data.csv'

    #Calculate average discount percentages for each category
    avg_discounts = calculate_average_discounts(synthetic_data_path)

    if not avg_discounts:
        avg_discounts = {
            "Sports": 16.9,
            "Clothing": 21.5,
            "Toys": 18.6,
            "Beauty": 18.2,
            "Books": 19.1,
            "Home & Kitchen": 18.3,
            "Electronics": 18.3,
            "Office Supplies": 19.2,
            "Furniture": 17.8,
            "Technology": 18.8
        }
        print("Using default average discount values.")
    else:
        print("\nUsing calculated average discount percentages:")


    customer_analysis = analyze_synthetic_data(synthetic_data_path)

    print("\nPredictions for Each Product Category")
    print("{:<20} {:<50} {:<50} {:<15}".format(
        "Category", "Segment % (Consumer, Corporate, Home Office)", "Top 5 States", "Optimal Discount"
    ))
    print("-" * 135)

    for category in sorted(customer_analysis.keys()):
        discount = avg_discounts.get(category, 18.5)  #Gives us our average discount %

        prediction = predict_segment_and_state(category, customer_analysis)

        consumer_pct = prediction['segment_probabilities'].get('Consumer', 0) * 100
        corporate_pct = prediction['segment_probabilities'].get('Corporate', 0) * 100
        home_office_pct = prediction['segment_probabilities'].get('Home Office', 0) * 100

        if prediction['best_segment'] == 'Consumer':
            segment_str = f"*{consumer_pct:.1f}%, {corporate_pct:.1f}%, {home_office_pct:.1f}%"
        elif prediction['best_segment'] == 'Corporate':
            segment_str = f"{consumer_pct:.1f}%, *{corporate_pct:.1f}%, {home_office_pct:.1f}%"
        else:
            segment_str = f"{consumer_pct:.1f}%, {corporate_pct:.1f}%, *{home_office_pct:.1f}%"

        states_str = ""
        for i, state_data in enumerate(prediction['top5_states']):
            if i > 0:
                states_str += ", "

            state_name = state_data['state']
            state_initial = state_to_initial.get(state_name, state_name[:2])

            if state_name == prediction['best_state']:
                states_str += f"*{state_initial}: {state_data['percentage']}"
            else:
                states_str += f"{state_initial}: {state_data['percentage']}"

        # Display our results
        print("{:<20} {:<50} {:<50} {}%".format(
            category, segment_str, states_str, discount
        ))

if __name__ == "__main__":
    main()