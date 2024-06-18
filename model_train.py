import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv("world_population_data.csv")

ukraine_data = data[data['country'] == 'Ukraine'][["2000 population", "2010 population", "2015 population", "2020 population", "2022 population", "2023 population"]]
ukraine_data = ukraine_data.melt(var_name='Year', value_name='Population')
ukraine_data['Year'] = ukraine_data['Year'].str.extract('(\d+)').astype(int)
ukraine_data['Population'] = ukraine_data['Population'].astype(float)

X = ukraine_data['Year'].values.reshape(-1, 1)
y = ukraine_data['Population'].values

model = LinearRegression()
model.fit(X, y)

years_to_predict = [2030, 2035, 2040]
predictions = model.predict(np.array(years_to_predict).reshape(-1, 1))

prediction_data = pd.DataFrame({
    'Year': years_to_predict,
    'Predicted Population': predictions
})
prediction_data.to_csv("ukraine_population_predictions.csv", index=False)

for year, population in zip(years_to_predict, predictions):
    print(f"Predicted population for Ukraine in {year}: {population:.2f}")

# Plotting the results
plt.figure(figsize=(10, 5))
plt.scatter(ukraine_data['Year'], ukraine_data['Population'], color='blue', label='Actual Population')
plt.plot(ukraine_data['Year'], model.predict(X), color='red', label='Fitted Line')
plt.scatter(years_to_predict, predictions, color='green', marker='x', s=100, label='Predictions')
plt.xlabel('Year')
plt.ylabel('Population')
plt.title('Population Prediction for Ukraine')
plt.legend()
plt.grid(True)
plt.show()
