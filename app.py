from flask import Flask

app = Flask(__name__)

@app.route('/hello')
def hello():
    print("Handling /hello request")  # Explicit log
    return "Hello, World from Flask!"

if __name__ == '__main__':
    try:
        print("Starting Flask app on 0.0.0.0:5000")  # Explicit startup log
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting Flask app: {e}")  # Log any exceptions