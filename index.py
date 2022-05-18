from flask import Flask, request, render_template
from os.path import exists

app = Flask(__name__)

def file_reading(filename):
    with open("Python_test_jr/"+filename+'.txt') as file:
        lines = file.readlines()
    return lines

def fetch_text_by_lines(file_data, start=None, end=None):
    result = ""
    if start is not None:
        if start > 0:
            start = start -1
        if end:
            if start > end:
                result = ["Start line number should be higher than end line number"]
            else:
                result = file_data[start:end]
        else:
            result = file_data[start:]
    elif end is not None:
        if end>0:
            result = file_data[:end]
        else:
            result = ["End line number should be higher than 0"]
    else:
        result = file_data
    return result

def check_positions(start,end):
    if start is not None:
        start = int(start)
    if end is not None:
        end = int(end)
    return start, end

@app.route('/app')
@app.route('/app/<file>', methods=['GET'])
def reader(file = "file1"):
    file_exists = exists("Python_test_jr/"+file+".txt")
    if file_exists:
        response = file_reading(file)
        args = request.args
        start_line = args.get('start')
        end_line = args.get('end')
        start_line, end_line = check_positions(start_line, end_line)
        display_file = fetch_text_by_lines(response,start=start_line, end=end_line)
    else:
        display_file= ["File does not exist! Please give valid file name"]
    return render_template('index.html', response_obj=display_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)