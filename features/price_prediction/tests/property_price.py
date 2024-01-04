import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from category_encoders import TargetEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Load your generated dataset
df = pd.read_csv("property_data.csv")

duplicates = df.apply(lambda x: x.duplicated()).sum()
# print (duplicates)
data = df.drop_duplicates()


# Drop the 'property_name' column
data = data.drop(columns=['property_name'])

numeric_data= data.select_dtypes(include=[np.number])
categorical_data = data.select_dtypes(exclude=[np.number])
print ("There are {} numeric and {} categorical columns in dataset"
.format(numeric_data.shape[1],categorical_data.shape[1]))


# Visualize relationships between numerical features and target using scatter plots
numerical_features = ['number_of_bedrooms', 'bedroom_size', 'bathrooms', 'cleaning_fee', 'beds']
for feature in numerical_features:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data[feature], y=data['base_price'])
    plt.title(f'Relationship between {feature} and Base Price')
    plt.show()

# Visualize relationships between categorical features and target using box plots
categorical_features = ['property_type', 'seasonality', 'bed_type', 'cancellation_policy', 'neighborhood']
for feature in categorical_features:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=data[feature], y=data['base_price'])
    plt.title(f'Relationship between {feature} and Base Price')
    plt.xticks(rotation=45)
    plt.show()


# Impute missing values with mean for numerical features
numerical_features = ['number_of_bedrooms', 'bedroom_size', 'bathrooms', 'cleaning_fee', 'beds']
data[numerical_features] = data[numerical_features].fillna(data[numerical_features].mean())

# Impute missing values with mode for categorical features
categorical_features = ['location','property_type', 'amenities', 'seasonality', 'bed_type', 'cancellation_policy', 'neighborhood']
data[categorical_features] = data[categorical_features].fillna(data[categorical_features].mode().iloc[0])

# # Convert categorical features using one-hot encoding
# data_encoded = pd.get_dummies(data, columns=categorical_features)
# # Convert True and False to 1 and 0
# data_encoded = data_encoded.astype(int)

label_encoder = LabelEncoder()
for feature in categorical_features:
    data[feature] = label_encoder.fit_transform(data[feature])

# Calculate correlation matrix for all features
# all_features = numerical_features + list(data_encoded.columns)
correlation_matrix = data.corr()

# Create a heatmap
plt.figure(figsize=(20, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

data.head(2)

# Create interaction terms
data['bedrooms_bathrooms_interaction'] = data['number_of_bedrooms'] * data['bathrooms']

# Create polynomial features
data['beds_squared'] = data['beds'] ** 2

# Create derived ratios
data['price_per_bedroom'] = data['base_price'] / data['number_of_bedrooms']


# Remove extreme outliers in base_price
data = data[data['base_price'] < 5000]


# Transformation
data['log_base_price'] = np.log(data['base_price'])

# Try Different Regression Models
X = data.drop(columns=['base_price', 'log_base_price'])
y = data['log_base_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X.head(2)

y.head(2)

# Initialize StandardScaler
scaler = StandardScaler()

# Fit and transform the scaler on training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform the test data using the same scaler
X_test_scaled = scaler.transform(X_test)

models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Random Forest Regressor": RandomForestRegressor(random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(random_state=42)
}

for model_name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"{model_name} - MSE: {mse:.4f}, R-squared: {r2:.4f}")


# Stacking Ensemble
base_models = [
    ('linear', LinearRegression()),
    ('ridge', Ridge(alpha=1.0)),
    ('random_forest', RandomForestRegressor(random_state=42)),
    ('gradient_boosting', GradientBoostingRegressor(random_state=42))
]
stacking_model = StackingRegressor(estimators=base_models, final_estimator=LinearRegression())
stacking_model.fit(X_train_scaled, y_train)
y_pred_stacking = stacking_model.predict(X_test_scaled)
mse_stacking = mean_squared_error(y_test, y_pred_stacking)
print(f"Stacking Ensemble Mean Squared Error: {mse_stacking:.4f}")

# Blending Ensemble
base_model_1 = RandomForestRegressor(random_state=42)
base_model_2 = GradientBoostingRegressor(random_state=42)
base_model_1.fit(X_train_scaled, y_train)
base_model_2.fit(X_train_scaled, y_train)
blend_preds_base_1 = base_model_1.predict(X_test_scaled)
blend_preds_base_2 = base_model_2.predict(X_test_scaled)
blend_features = pd.DataFrame({
    'BaseModel1': blend_preds_base_1,
    'BaseModel2': blend_preds_base_2
})
blend_model = LinearRegression()
blend_model.fit(blend_features, y_test)
blend_predictions = blend_model.predict(blend_features)
mse_blend = mean_squared_error(y_test, blend_predictions)
print(f"Blending Ensemble Mean Squared Error: {mse_blend:.4f}")

# Visualize the predictions
plt.scatter(y_test, y_pred_stacking)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.title("True Values vs Predictions (Stacking Ensemble)")
plt.show()
