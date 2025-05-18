import pandas as pd
import numpy as np
import random
import uuid

def generate_synthetic_data(num_records=1000):
    #Combines the categories from each set
    categories = [
        "Office Supplies",
        "Furniture",
        "Technology",
        "Books",
        "Home & Kitchen",
        "Electronics",
        "Beauty",
        "Toys",
        "Clothing",
        "Sports"
    ]

    #Defines the customer segments
    customer_segments = ["Consumer", "Corporate", "Home Office"]

    #Tells us our top customer states that are relevant
    states_list = [
        "California", "New York", "Texas", "Pennsylvania", "Washington",
        "Illinois", "Florida", "Ohio", "Georgia", "Michigan"
    ]

    #Applies weighted probabilities to states that match it to real world distribution
    #There are higher weights for states with more commercial activity
    state_weights_raw = [0.20, 0.11, 0.10, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03]
    state_weights = [w/sum(state_weights_raw) for w in state_weights_raw]  #Makes sure sums add up to 1

    #Various product names for different categories
    product_templates = {
        "Office Supplies": ["Pen Set", "Notebook", "Paper Clips", "Stapler", "Binder", "Desk Organizer", "File Cabinet"],
        "Furniture": ["Desk", "Chair", "Bookcase", "Table", "Sofa", "Cabinet", "Drawer"],
        "Technology": ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones"],
        "Books": ["Novel", "Textbook", "Biography", "Cookbook", "Self-Help Book", "Reference Guide", "Children's Book"],
        "Home & Kitchen": ["Blender", "Cookware", "Utensils", "Dinnerware", "Toaster", "Coffee Maker", "Knife Set"],
        "Electronics": ["Television", "Camera", "Speaker", "Charger", "Smartwatch", "Gaming Console", "Printer"],
        "Beauty": ["Makeup", "Skincare", "Haircare", "Fragrance", "Beauty Tool", "Nail Polish", "Face Mask"],
        "Toys": ["Action Figure", "Board Game", "Puzzle", "Doll", "Building Blocks", "Remote Control Car", "Educational Toy"],
        "Clothing": ["Shirt", "Pants", "Dress", "Jacket", "Sweater", "Shoes", "Accessories"],
        "Sports": ["Ball", "Training Equipment", "Racket", "Shoes", "Apparel", "Protection Gear", "Fitness Tracker"]
    }

    #Different price ranges per category
    price_ranges = {
        "Office Supplies": (5, 100),
        "Furniture": (50, 500),
        "Technology": (100, 1000),
        "Books": (10, 50),
        "Home & Kitchen": (20, 200),
        "Electronics": (50, 800),
        "Beauty": (10, 150),
        "Toys": (15, 80),
        "Clothing": (20, 200),
        "Sports": (15, 300)
    }

    #Gives us segment probabilities based off our analysis
    segment_probabilities = {
        "Office Supplies": {"Consumer": 0.52, "Corporate": 0.30, "Home Office": 0.18},
        "Furniture": {"Consumer": 0.52, "Corporate": 0.31, "Home Office": 0.17},
        "Technology": {"Consumer": 0.51, "Corporate": 0.30, "Home Office": 0.19},
        "Books": {"Consumer": 0.52, "Corporate": 0.30, "Home Office": 0.18},
        "Home & Kitchen": {"Consumer": 0.52, "Corporate": 0.31, "Home Office": 0.17},
        "Electronics": {"Consumer": 0.51, "Corporate": 0.30, "Home Office": 0.19},
        "Beauty": {"Consumer": 0.51, "Corporate": 0.30, "Home Office": 0.19},
        "Toys": {"Consumer": 0.52, "Corporate": 0.30, "Home Office": 0.18},
        "Clothing": {"Consumer": 0.52, "Corporate": 0.31, "Home Office": 0.17},
        "Sports": {"Consumer": 0.52, "Corporate": 0.31, "Home Office": 0.17}
    }

    #Different lists to store our data
    customer_ids = []
    product_names = []
    product_categories = []
    customer_states_data = []
    customer_segments_data = []
    prices = []

    #Generates the data
    for _ in range(num_records):
        category = random.choice(categories)

        customer_id = f"CUST-{uuid.uuid4().hex[:8].upper()}"

        product_base = random.choice(product_templates[category])
        product_name = f"{product_base} {random.choice(['Premium', 'Standard', 'Basic', 'Pro', 'Deluxe', 'Essential'])}"

        state = np.random.choice(states_list, p=state_weights)

        segment_probs = segment_probabilities[category]
        segment = np.random.choice(
            list(segment_probs.keys()),
            p=list(segment_probs.values())
        )

        min_price, max_price = price_ranges[category]
        price = round(random.uniform(min_price, max_price), 2)

        customer_ids.append(customer_id)
        product_names.append(product_name)
        product_categories.append(category)
        customer_states_data.append(state)
        customer_segments_data.append(segment)
        prices.append(price)

    #Create a DataFrame
    df = pd.DataFrame({
        'Customer_ID': customer_ids,
        'Product_Name': product_names,
        'Category': product_categories,
        'Customer_State': customer_states_data,
        'Customer_Segment': customer_segments_data,
        'Price': prices
    })

    return df

if __name__ == "__main__":
    #Generate the synthetic data
    num_records = 5000
    synthetic_data = generate_synthetic_data(num_records)

    print("\nCategory distribution:")
    category_counts = synthetic_data['Category'].value_counts()
    for category, count in category_counts.items():
        print(f"{category}: {count}")

    print("\nCustomer segment distribution:")
    segment_counts = synthetic_data['Customer_Segment'].value_counts(normalize=True).round(3) * 100
    for segment, percentage in segment_counts.items():
        print(f"{segment}: {percentage}%")

    print("\nCustomer state distribution:")
    state_counts = synthetic_data['Customer_State'].value_counts().head(10)
    for state, count in state_counts.items():
        print(f"{state}: {count}")

    synthetic_data.to_csv('synthetic_ecommerce_data.csv', index=False)
    print("\nSaved synthetic data to 'synthetic_ecommerce_data.csv'")