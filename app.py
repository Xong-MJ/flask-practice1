from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return f"<a href='{url_for('about')}'>소개로</a>"

@app.route("/main")
def home():
    return "<h1>메인 페이지</h1>"

@app.route('/hello')  # 주소 둘을
@app.route('/hello/<name>')  # 한 함수에
def hello(name=None):  # 기본값이 있어야 합니다
    if name:
        return f'안녕하세요, {name} 님'
    return '안녕하세요'

@app.route("/about")
def about():
    return '소개 페이지'

@app.route("/test/<text>")
def route_sample(text):
    return f"<h1>{text}</h1>"

@app.route("/age/<num>")  # 타입 없음
def age_any(num):
    return f"<h1>{num} 살 - 타입은 {type(num).__name__}</h1>"

@app.route("/age2/<int:num>")  # 정수만
def age_int(num):
    return f"<h1>{num} 살 - 타입은 {type(num).__name__}</h1>"

@app.route("/hi/<name>")
def hi_template_render(name):
    return render_template("hi.html", name=name)

@app.route('/user/<username>')
def profile(username):
    return render_template('profile.html', username=username,
                            posts=['첫 글', '두 번째 글'])

@app.route('/newuser/<username>')
def new_user(username):
    return render_template('profile.html', username=username, posts=[])

@app.route('/post/<int:pid>')
def post(pid):
    return f'{pid}번 글 (자료형: {type(pid).__name__})'

@app.route('/notes/')  # 끝에 슬래시
def notes():
    return '메모 목록'

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', '1')
    if not query:
        return '검색어를 입력하세요'
    return f'"{query}" 검색 결과 ({page} 페이지)'

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        banana = request.form['banana']
        melon = request.form['melon']
        return (f'banana = {banana} ({type(banana).__name__}) / '
                f'melon = {melon} ({type(melon).__name__})')
    return '''
    <form method="post">
        <input type="text" name="banana">
        <input type="number" name="melon">
        <button type="submit">보내기</button>
    </form>'''

@app.route('/attach', methods=['GET', 'POST'])
def attach():
    if request.method == 'POST':
        f = request.files.get('cherry')
        if f is None:
            return 'cherry 가 files 에 없습니다'
        return f'{f.filename} / {len(f.read())} 바이트'
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="text" name="banana">
        <input type="file" name="cherry">
        <button type="submit">보내기</button>
    </form>'''

if __name__ == "__main__":
    app.run(debug=True)
