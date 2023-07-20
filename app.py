from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        # Get the filename from the uploaded file
        filename = file.filename
        # Construct the full file path including the filename
        file_path = os.path.join("C:\\Users\\Arham\\Desktop\\Timetable", filename)
        # Save the file to the desired location
        file.save(file_path)
        return jsonify({'message': 'Timetable generated successfully!!'}), 200
    else:
        return jsonify({'error': 'Error generating timetable.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
