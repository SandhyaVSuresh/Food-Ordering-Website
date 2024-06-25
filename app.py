from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'foodorder'

mysql = MySQL(app)

username = ""
quantity = ""
resname = ""
tot = 0
restaurantn = ""


@app.route('/', methods=['GET', 'POST'])
def front():
    msg = ''
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM restaurant')
    rest = cursor.fetchall()
    cursor.close()

    return render_template('front.html', msg=msg, rest=rest)


@app.route('/log', methods=['GET', 'POST'])
def log():
    global username
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT count(*) from register WHERE uname = %s AND pwd = %s", (username, password))
        row = cursor.fetchone()
        cursor.execute('SELECT * FROM restaurant')
        rest = cursor.fetchall()
        print(row, type(row))
        cursor.close()
        if row[0] == 1:
            msg = ''
            return render_template('front.html', msg=msg, username=username, rest=rest)
        else:
            return render_template('log.html', msg='Invalid username or password')
    else:
        return render_template('log.html', msg='', username=username)


@app.route('/logres', methods=['GET', 'POST'])
def logres():
    global resname
    if request.method == 'POST':
        resname = request.form['uname']
        password = request.form['pwd']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT count(*) from restaurant WHERE username = %s AND password = %s", (resname, password))
        row = cursor.fetchone()
        print(row, type(row))
        cursor.close()
        if row[0] == 1:
            msg = ''
            return render_template('res_board.html', msg=msg, resname=resname)
        else:
            return render_template('logres.html', msg='Invalid username or password')
    else:
        return render_template('logres.html', msg='', resname=resname)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        emailid = request.form['emailid']
        phno = request.form['phno']
        dob = request.form['dob']
        addr = request.form['addr']
        uname = request.form['uname']
        pwd = request.form['pwd']
        cursor = mysql.connection.cursor()
        a = cursor.execute(
            '''INSERT INTO register 
            (fname, lname, emailid, phno, dob, addr, uname, pwd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
            (fname, lname, emailid, phno, dob, addr, uname, pwd))
        if a > 0:
            msg = "registered"
        else:
            msg = "not registered"
        mysql.connection.commit()
        cursor.close()
        return render_template('register.html', msg=msg)


@app.route('/register_details', methods=['GET', 'POST'])
def register_details():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT sino, fname, lname, emailid, phno, dob, addr, uname FROM register')
    users = cursor.fetchall()
    cursor.close()
    return render_template('register_details.html', users=users)


@app.route('/add_res', methods=['GET', 'POST'])
def add_res():
    if request.method == 'GET':
        return render_template('add_res.html')

    if request.method == 'POST':
        restaurantname = request.form['restaurantname']
        cityname = request.form['cityname']
        ownermanager = request.form['ownermanager']
        ownername = request.form['ownername']
        managername = request.form['managername']
        ohour = request.form['ohour']
        openingstate = request.form['openingstate']
        alcohol = request.form.get('alcohol')
        username = request.form['username']
        password = request.form['password']
        phno = request.form['phno']
        email = request.form['email']
        adhar = request.form['adhar']
        img = request.form['img']
        cursor = mysql.connection.cursor()
        a = cursor.execute(
            '''INSERT INTO restaurant (restaurantname,city, ownerormanager, ownername, managername, openhours, openstates,servesalcohol,username,password,phoneno,email,adhar,image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (restaurantname, cityname, ownermanager, ownername, managername, ohour, openingstate, alcohol, username, password, phno, email, adhar, img))
        if a > 0:
            msg = "registered"
        else:
            msg = "not registered"
        mysql.connection.commit()
        cursor.close()
        return render_template('add_res.html', msg=msg)


@app.route('/updateres', methods=['POST', 'GET'])
def updateres():
    if request.method == 'POST':
        restaurantname = request.form['restaurantname']
        ownername = request.form['ownername']
        managername = request.form['managername']
        openstate = request.form.get('openstate')
        alcohol = request.form.get('alcohol')
        username = request.form['username']
        phno = request.form['phno']
        email = request.form['email']
        img = request.form['img']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE restaurant SET restaurantname=%s, ownername=%s, managername=%s, openstates=%s, servesalcohol=%s, username=%s, phoneno=%s, email=%s, image=%s
        WHERE restaurantname=%s
        """, (restaurantname, ownername, managername, openstate, alcohol, username, phno, email, img, restaurantname))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('res_details'))


@app.route('/deleteres/<string:restaurantname>', methods=['GET'])
def deleteres(restaurantname):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM restaurant WHERE restaurantname=%s", (restaurantname,))
    mysql.connection.commit()
    return redirect(url_for('res_details'))


@app.route('/food1', methods=['GET', 'POST'])
def food1():
    return render_template('food1.html')


@app.route('/add_cart', methods=['GET', 'POST'])
def add_cart():
    global username, restaurantn
    if restaurantn != '':
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM restaurant where restaurantname=%s', (restaurantn,))
        title = cursor.fetchall()
        cursor.execute(
            'SELECT * FROM fooddetail where restaurantname=%s', (restaurantn,))
        users = cursor.fetchall()
        cursor.close()
        return render_template('food1.html', title=title, users=users, username=username, quantity=quantity, restaurantn=restaurantn)
    else:
        return render_template('food1.html', username=username, quantity=quantity)

    #return render_template('add_cart.html', users=users, username=username, quantity=quantity)


@app.route('/add_cart1/<string:restaurant>', methods=['GET', 'POST'])
def add_cart1(restaurant):
    global username, restaurantn
    restaurantn = restaurant
    return redirect(url_for('add_cart'))
    #return render_template('food1.html', users=users, username=username, quantity=quantity)


@app.route('/productcart')
def productcart():
    global username, quantity
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT foodimage,foodid,foodname,rate FROM fooddetail")
    users = cursor.fetchall()
    cursor.close()
    return render_template('add_cart.html', users=users, username=username, quantity=quantity)


@app.route('/cart', methods=['POST'])
def cart():
    global username
    res = request.form.get('hotel')
    quantity = request.form.get('quantity')
    foodid = request.form.get('fid')
    foodname = request.form.get('fname')
    rate = request.form.get('rate')
    cur = mysql.connection.cursor()
    cur.execute(
        '''INSERT INTO cart (username, foodid, foodname, qty, rate, restaurantname) VALUES (%s,%s,%s,%s,%s,%s)''',
        (username, foodid, foodname, quantity, rate, res))
    mysql.connection.commit()
    return redirect(url_for('add_cart'))


@app.route('/cart_remove', methods=['GET', 'POST'])
def cart_remove():
    global username
    cur = mysql.connection.cursor()
    cur.execute('''SELECT c.foodid, c.foodname, f.rate, c.qty, f.foodimage
                       FROM cart c 
                       JOIN fooddetail f ON c.foodid = f.foodid 
                       WHERE c.username = %s''', (username,))
    users = cur.fetchall()
    cur.close()
    return render_template('cart_remove.html', users=users)


@app.route('/checkcart', methods=['GET', 'POST'])
def checkcart():
    global tot, username
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(rate * qty) AS total FROM cart WHERE username = %s", (username,))
    tot = cur.fetchall()
    cur.execute("SELECT foodid,foodname,rate,qty FROM cart WHERE username = %s", (username,))
    users = cur.fetchall()
    mysql.connection.commit()
    return render_template('checkcart.html', users=users, tot=tot)


@app.route('/deletecart/<int:foodid>', methods=['GET'])
def deletecart(foodid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cart WHERE foodid=%s", (foodid,))
    mysql.connection.commit()
    return redirect(url_for('cart_remove'))


@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT restaurantname FROM restaurant')
        options = cursor.fetchall()
        cursor.close()
        return render_template('add_food.html', options=options)

    if request.method == 'POST':
        print(request.form)
        foodname = request.form.get('foodname')
        fid = request.form.get('fid')
        cate = request.form.get('cate')
        discription = request.form.get('discription')
        rate = request.form.get('rate')
        restaurantname = request.form.get('restaurantname')
        foodtype = request.form.get('foodtype')
        ava = request.form.get('ava')
        img1 = request.form.get('img1')
        print(foodname, fid, cate, discription, rate, restaurantname, foodtype, ava, img1)
        cursor = mysql.connection.cursor()
        a = cursor.execute(
            '''INSERT INTO fooddetail VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (foodname, fid, cate, discription, rate, restaurantname, foodtype, ava, img1))
        if a > 0:
            msg = "registered"
        else:
            msg = "not registered"
        mysql.connection.commit()
        cursor.close()
        return render_template('add_food.html', msg=msg)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg = ''
    print(request)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(password, username)
        if username == 'admin' and password == '123':
            print("log in")
            return redirect('/admin_board')
        else:
            print('fail')
    return render_template('admin.html', msg=msg)


@app.route('/dashboard')
def dashboard():
    msg = ''
    return render_template('dashboard.html', msg=msg)


@app.route('/admin_board')
def admin_board():
    msg = ''
    return render_template('admin_board.html', msg=msg)


@app.route('/res_details', methods=['GET', 'POST'])
def res_details():
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT restaurantname, ownername, managername, openstates, servesalcohol, username, phoneno, email, image FROM restaurant')
    users = cursor.fetchall()
    cursor.close()
    return render_template('res_details.html', users=users)


@app.route('/updatereg', methods=['POST', 'GET'])
def updatereg():
    if request.method == 'POST':
        sino = request.form['sino']
        fname = request.form['fname']
        lname = request.form['lname']
        emailid = request.form['emailid']
        phno = request.form['phno']
        dob = request.form['dob']
        addr = request.form['addr']
        uname = request.form['uname']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE register SET sino=%s, fname=%s, lname=%s, emailid=%s, phno=%s, dob=%s, addr=%s, uname=%s
        WHERE fname=%s
        """, (sino, fname, lname, emailid, phno, dob, addr, uname, fname))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('register_details'))


@app.route('/deletereg/<string:fname>', methods=['GET'])
def deletereg(fname):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM register WHERE fname=%s", (fname,))
    mysql.connection.commit()
    return redirect(url_for('register_details'))


@app.route('/food_details')
def food_details():
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT foodname, foodid, category, discription, rate, restaurantname, foodtype, available, foodimage FROM fooddetail')
    users = cursor.fetchall()
    cursor.close()
    return render_template('food_details.html', users=users)


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        fid = request.form['fid']
        name = request.form['fname']
        cate = request.form['cate']
        dis = request.form['discription']
        rate = request.form['rate']
        restaurantname = request.form['restaurantname']
        foodtype = request.form['foodtype']
        ava = request.form['ava']
        img1 = request.form['img1']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE fooddetail SET foodname=%s, category=%s, discription=%s, rate=%s, restaurantname=%s, foodtype=%s, available=%s, foodimage=%s
        WHERE foodid=%s
        """, (name, cate, dis, rate, restaurantname, foodtype, ava, img1, fid))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('food_details'))


@app.route('/delete/<string:fid>', methods=['GET'])
def delete(fid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM fooddetail WHERE foodid=%s", (fid,))
    mysql.connection.commit()
    return redirect(url_for('food_details'))


@app.route('/gpay')
def gpay():
    global tot, username
    cur = mysql.connection.cursor()
    cur.execute("SELECT SUM(rate * qty) AS total FROM cart WHERE username = %s", (username,))
    tot = cur.fetchall()
    cur.close()
    return render_template('gpay.html', tot=tot, username=username)


@app.route('/card', methods=['POST', 'GET'])
def card():
    global tot, username

    if request.method == 'GET':
        return render_template('card.html', tot=tot, username=username)

    if request.method == 'POST':
        cardno = request.form.get('cardno')
        cvv = request.form.get('cvv')
        cardowner = request.form.get('cardowner')
        expiry = request.form.get('expiry')
        amount = request.form.get('amount')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT SUM(rate * qty) AS total FROM cart WHERE username = %s", (username,))
        tot = cursor.fetchall()
        cursor.execute(
            '''INSERT INTO card (username, cardno, cvv, cardowner, expiry, amount) VALUES (%s,%s,%s,%s,%s,%s)''',
            (username, cardno, cvv, cardowner, expiry, amount))
        mysql.connection.commit()
        cursor.close()
        return render_template('checkform.html', tot=tot, username=username)


@app.route('/cashondelivery', methods=['POST', 'GET'])
def cashondelivery():
    global tot, username
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT SUM(rate * qty) AS total FROM cart WHERE username = %s", (username,))
    tot = cursor.fetchall()
    cursor.close()
    return render_template('cashondelivery.html', tot=tot, username=username)


@app.route('/checkform', methods=['POST', 'GET'])
def checkform():
    global tot, username
    cur = mysql.connection.cursor()
    cur.execute("SELECT foodid,foodname,rate,qty FROM cart WHERE username = %s", (username,))
    users = cur.fetchall()
    cur.execute("SELECT SUM(rate * qty) AS total FROM cart WHERE username = %s", (username,))
    tot = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('checkform.html', users=users, username=username, tot=tot)


@app.route('/dashboardres')
def dashboardres():
    msg = ''
    return render_template('dashboardres.html', msg=msg)


@app.route('/res_board')
def res_board():
    msg = ''
    return render_template('res_board.html', msg=msg)


@app.route('/res_food')
def res_food():
    global resname
    cur = mysql.connection.cursor()
    cur.execute('''SELECT f.foodname,f.foodid,f.category,f.discription, f.rate,r.restaurantname, f.foodtype, f.available, f.foodimage
                           FROM restaurant r 
                           JOIN fooddetail f ON r.restaurantname = f.restaurantname
                           WHERE r.username = %s''', (resname,))
    users = cur.fetchall()
    cur.close()
    return render_template('res_food.html', users=users)


@app.route('/order_det', methods=['POST', 'GET'])
def order_det():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT c.username,c.foodid,c.foodname,c.rate, c.qty
                               FROM restaurant r 
                               JOIN cart c ON r.restaurantname = c.restaurantname
                               WHERE r.username = %s''', (resname,))
    users = cur.fetchall()
    cur.close()
    return render_template('order_det.html',users=users)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
