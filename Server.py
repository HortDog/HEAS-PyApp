from flask import Flask, request
recording = "False"

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def handle_post():
    global recording
    # Print the incoming request's body to the console
    decoded_data = request.data.decode()
    print(decoded_data)
    if decoded_data == '{"button":"rec_start"}': recording = "True"
    elif decoded_data == '{"button":"rec_stop"}': recording = "False"
    elif decoded_data == '{"button":"takepic"}':
        with open('Capture.txt', 'w') as file:
            file.write('a')
            file.close()
    # You can also access form data using request.form['name']
    with open('Record_condition.txt', 'w') as file:
        file.write(f"{recording}")
        file.close()

    # Respond to the ESP32
    return {"response": "Data received"}, 200



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)