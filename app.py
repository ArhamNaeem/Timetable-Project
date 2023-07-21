from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload-timetable', methods=['POST'])
def upload_timetableFile():
    file = request.files.get('file')
    if file:
        # Get the filename from the uploaded file
        filename = file.filename
        if not filename == 'subject.csv':
                 return jsonify({'error': f'File name {filename} is not acceptable'}), 400

        file_path = os.path.join("C:\\Users\\Arham\\Desktop\\Timetable", filename)
        # Save the file to the desired location
        file.save(file_path)
        return jsonify({'message': 'Timetable generated successfully!!'}), 200
    else:
        return jsonify({'error': 'Error generating timetable.'}), 400

@app.route('/upload-attendance', methods=['POST'])
def upload_attendanceFile():
    file = request.files.get('file')
    if file:
        # Get the filename from the uploaded file
        filename = file.filename
        if not filename == 'attendance.csv':
                 return jsonify({'error': f'File name {filename} is not acceptable'}), 400

        file_path = os.path.join("C:\\Users\\Arham\\Desktop\\Timetable", filename)
        # Save the file to the desired location
        file.save(file_path)
        return jsonify({'message': 'Attendance record added successfully!!'}), 200
    else:
        return jsonify({'error': 'Error uploading attendance record.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
