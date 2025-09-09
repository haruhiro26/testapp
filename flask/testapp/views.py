from flask import render_template, request, redirect, url_for
from testapp import app
from random import randint
from testapp import db
from testapp.models.employee import Employee

@app.route('/')
def index():
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
}
    deta = 'views.pyのinsert_something部分です。'
    return render_template('testapp/index.html', my_dict=my_dict)

@app.route('/test')
def other1():
    return render_template('testapp/index2.html')

@app.route('/sampleform', methods=['GET', 'POST'])
def sample_form():
    if request.method == 'GET':
        return render_template('testapp/sampleform.html')
    if request.method == 'POST':
        hands = {
            '0': 'グー',
            '1': 'チョキ',
            '2': 'パー'
        }
        janken_mapping = {
            'draw': '引き分け',
            'win': '勝ち',
            'lose': '負け'
        }

        player_hand_ja = hands[request.form['janken']]
        player_hand = int(request.form['janken'])
        enemy_hand = randint(0,2)
        enemy_hand_ja = hands[str(enemy_hand)]
        if player_hand == enemy_hand:
            judgement = 'drow'
        elif (player_hand == 0 and enemy_hand == 1) or (player_hand == 1 and enemy_hand == 2) or (player_hand == 2 and enemy_hand == 0):
            judgement = 'win'
        else:
            judgement = 'lose'
        print(f'じゃんけん開始： enemy_hand: {enemy_hand}, player_hand:{player_hand}, judgement:{judgement}')
        return f'相手： {enemy_hand_ja}, あなた： {player_hand_ja}, 判定： {janken_mapping[judgement]}'
    
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('testapp/add_employee.html')
    if request.method == 'POST':
        form_name = request.form.get('name')
        form_mail = request.form.get('mail')

        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')

        form_year = request.form.get('year', default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
    db.session.add(employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/employees')
def employee_list():
    employees = Employee.query.all()
    return render_template('testapp/employee_list.html', employees=employees)

@app.route('/employees/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('testapp/employee_detail.html', employee=employee)

@app.route('/employees/<int:id>/edit', methods=['GET'])
def employee_edit(id):
    employee = Employee.query.get(id)
    return render_template('testapp/employee_edit.html', employee=employee)

@app.route('/employees/<int:id>/update', methods=['POST'])
def employee_update(id):
    employee = Employee.query.get(id)
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))

@app.route('/employees/<int:id>/delete', methods=['POST'])
def employee_delete(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employee_list'))