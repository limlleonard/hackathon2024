import os
from flask import Flask, render_template, request, redirect, jsonify
from funk import Embeder

dir_pdf='./files'
os.makedirs(dir_pdf, exist_ok=True)
api1=os.getenv('openai_api')
embeder1=Embeder(dir_pdf)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print('upload')
    """pdf Dateien im vorgegebene Ordner einfügen für später zusammenzufassen"""
    if 'file' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('file')
    lst_filename=[]
    for file in files:
        if file.filename == '':
            continue
        print(file)
        file.save(os.path.join(dir_pdf, file.filename))
        lst_filename.append(file.filename)
    app.config['dir_src']=''
    return jsonify({'lst_filename':lst_filename})
    # return redirect(url_for('index'))

@app.route('/delete_pdf', methods=['POST'])
def delete_pdf():
    """Inhalt vom pdf Ordner löschen"""
    folder = dir_pdf
    # reset qa
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    return jsonify({'lst_filename':[]})
    # return redirect(url_for('index'))

@app.route('/embed_pdf', methods=['POST'])
def embed_pdf():
    """embed pdf"""
    embeder1.init_llama(api1)
    embeder1.embed()
    return jsonify({'lst_filename':[]})
    # return redirect(url_for('index'))

@app.route('/ask', methods=['POST'])
def ask():
    """ask a question"""
    frg1 = request.get_json().get("text", "")
    ant1 = embeder1.qa(frg1)
    return jsonify(ant1=ant1)


if __name__ == '__main__':
    app.run(debug=True)