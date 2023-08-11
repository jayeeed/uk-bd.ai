import csv
from faker import Faker
import random

fake = Faker()

# "location",

property_fields = [
    "property_id", "property_type", "number_of_bedrooms", "amenities",
    "seasonality", "base_price", "estimated_monthly_bookings", "bathrooms",
    "bed_type", "cancellation_policy", "cleaning_fee", "host_response_rate",
    "number_of_reviews", "review_scores_rating", "beds"
]

amenities_list = ["Internet", "Gym", "AC", "Laundry", "BBQ", "Stove", "Fridge"]

def generate_property_data(property_id):
    return {
        "property_id": property_id,
        # "location": fake.city(),
        "property_type": random.choice(["Apartment", "House", "Villa"]),
        "number_of_bedrooms": random.randint(1, 5),
        "amenities": random.sample(amenities_list, random.randint(1, 7)),
        "seasonality": random.choice(["Summer", "Winter", "Autumn"]),
        "base_price": random.randint(20, 500),
        "estimated_monthly_bookings": random.randint(1, 30),
        "bathrooms": random.randint(1, 4),
        "bed_type": random.choice(["Single", "Double", "Queen", "King"]),
        "cancellation_policy": random.choice(["Flexible", "Moderate", "Strict"]),
        "cleaning_fee": random.randint(10, 50),
        "host_response_rate": random.randint(20, 100),
        "number_of_reviews": random.randint(0, 200),
        # "review_scores_rating": round(random.uniform(2, 5), 2),
        "review_scores_rating": random.randint(2, 5),
        "beds": random.randint(1, 5)
    }

num_properties = 1000  # Change this to the desired number of properties
output_file = "property_data.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=property_fields)
    writer.writeheader()

    for property_id in range(1, num_properties + 1):
        property_data = generate_property_data(property_id)
        writer.writerow(property_data)

print(f"{num_properties} property records generated and saved to {output_file}.")
