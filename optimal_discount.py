import pandas as pd

def find_optimal_discounts(data_path):
    df = pd.read_csv(data_path)

    #Groups everything by category and discount percentage
    revenue_by_category_discount = df.groupby(['Category', 'Discount (%)'])['Final_Price(Rs.)'].sum().reset_index()

    optimal_discounts = {} #Used to store the best discount rates for each category

    #Done for each product category
    for category in df['Category'].unique():
        #Filters to only include the rows for the current category
        category_data = revenue_by_category_discount[revenue_by_category_discount['Category'] == category]

        max_revenue_idx = category_data['Final_Price(Rs.)'].idxmax() #Finds the row with the highest revenue using idmax()
        optimal_discount = category_data.loc[max_revenue_idx, 'Discount (%)'] #This tells us which discount percent had the best revenue, and extracts it

        optimal_discounts[category] = optimal_discount #Stores the results

    return optimal_discounts

def predict_optimal_discount(category, optimal_discounts):
    if category in optimal_discounts:
        return optimal_discounts[category] #If category is the same, it returns its optimal value
    else:
        return sum(optimal_discounts.values()) / len(optimal_discounts) #If category doesnt exist, it calculates the average of all the known discounts so we have a reasonable default

if __name__ == "__main__":
    data_path = '4thdataset.csv'

    #Find the optimal discounts for each category
    optimal_discounts = find_optimal_discounts(data_path)

    print("Optimal Discount Percentages by Category:")
    for category, discount in optimal_discounts.items():
        print(f"{category}: {discount}%") #Displays the results