from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
model = pickle.load(open("vot_reg.pkl", "rb"))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        
        # Handling Fuel Type
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        
        # Calculate car's age
        Year = 2020 - Year
        
        # Handling Seller Type
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        Seller_Type_Individual = 1 if Seller_Type_Individual == 'Individual' else 0

        # Handling Transmission Type
        Transmission_Manual = request.form['Transmission_Manual']
        Transmission_Manual = 1 if Transmission_Manual == 'Manual' else 0

        # Predicting price
        input_data = np.array([[Year, Present_Price, Kms_Driven, Owner, 
                                Fuel_Type_Diesel, Fuel_Type_Petrol, 
                                Seller_Type_Individual, Transmission_Manual]])
        prediction = model.predict(input_data)
        output = round(prediction[0], 2)

        if output < 0:
            return render_template('index.html', prediction_text="Sorry, you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You can sell the Car at {} lakhs".format(output))
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False)
