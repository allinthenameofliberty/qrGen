import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    nickname = db.Column(db.String(100), nullable=True)
    home_phone = db.Column(db.String(50), nullable=True)
    work_phone = db.Column(db.String(50), nullable=True)
    cell_phone = db.Column(db.String(50), nullable=True)
    fax = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100))
    work_email = db.Column(db.String(100), nullable=True)
    home_street = db.Column(db.String(200), nullable=True)
    home_city = db.Column(db.String(100), nullable=True)
    home_state = db.Column(db.String(100), nullable=True)
    home_postal_code = db.Column(db.String(20), nullable=True)
    home_country = db.Column(db.String(100), nullable=True)
    work_street = db.Column(db.String(200), nullable=True)
    work_city = db.Column(db.String(100), nullable=True)
    work_state = db.Column(db.String(100), nullable=True)
    work_postal_code = db.Column(db.String(20), nullable=True)
    work_country = db.Column(db.String(100), nullable=True)
    organization = db.Column(db.String(100))
    title = db.Column(db.String(100))
    role = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(200))
    work_url = db.Column(db.String(200), nullable=True)
    twitter = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    birthday = db.Column(db.String(10), nullable=True)
    anniversary = db.Column(db.String(10), nullable=True)
    note = db.Column(db.String(500), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)

def generate_contact_qr(contact):
    vcard = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"N:{contact.last_name};{contact.first_name}\n"
        f"FN:{contact.first_name} {contact.last_name}\n"
        f"NICKNAME:{contact.nickname}\n"
        f"TEL;TYPE=home:{contact.home_phone}\n"
        f"TEL;TYPE=work:{contact.work_phone}\n"
        f"TEL;TYPE=cell:{contact.cell_phone}\n"
        f"TEL;TYPE=fax:{contact.fax}\n"
        f"EMAIL;TYPE=work:{contact.work_email}\n"
        f"EMAIL:{contact.email}\n"
        f"ADR;TYPE=home:;;{contact.home_street};{contact.home_city};{contact.home_state};{contact.home_postal_code};{contact.home_country}\n"
        f"ADR;TYPE=work:;;{contact.work_street};{contact.work_city};{contact.work_state};{contact.work_postal_code};{contact.work_country}\n"
        f"ORG:{contact.organization}\n"
        f"TITLE:{contact.title}\n"
        f"ROLE:{contact.role}\n"
        f"URL;TYPE=work:{contact.work_url}\n"
        f"URL:{contact.url}\n"
        f"X-SOCIALPROFILE;TYPE=twitter:{contact.twitter}\n"
        f"X-SOCIALPROFILE;TYPE=linkedin:{contact.linkedin}\n"
        f"BDAY:{contact.birthday}\n"
        f"ANNIVERSARY:{contact.anniversary}\n"
        f"NOTE:{contact.note}\n"
        f"GEO:{contact.latitude},{contact.longitude}\n"
        "END:VCARD"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return img_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        contact = Contact(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            nickname=request.form['nickname'],
            home_phone=request.form['home_phone'],
            work_phone=request.form['work_phone'],
            cell_phone=request.form['cell_phone'],
            fax=request.form['fax'],
            email=request.form['email'],
            work_email=request.form['work_email'],
            home_street=request.form['home_street'],
            home_city=request.form['home_city'],
            home_state=request.form['home_state'],
            home_postal_code=request.form['home_postal_code'],
            home_country=request.form['home_country'],
            work_street=request.form['work_street'],
            work_city=request.form['work_city'],
            work_state=request.form['work_state'],
            work_postal_code=request.form['work_postal_code'],
            work_country=request.form['work_country'],
            organization=request.form['organization'],
            title=request.form['title'],
            role=request.form['role'],
            url=request.form['url'],
            work_url=request.form['work_url'],
            twitter=request.form['twitter'],
            linkedin=request.form['linkedin'],
            birthday=request.form['birthday'],
            anniversary=request.form['anniversary'],
            note=request.form['note'],
            latitude=request.form['latitude'],
            longitude=request.form['longitude']
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('index'))
    
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.first_name = request.form['first_name']
        contact.last_name = request.form['last_name']
        contact.nickname = request.form['nickname']
        contact.home_phone = request.form['home_phone']
        contact.work_phone = request.form['work_phone']
        contact.cell_phone = request.form['cell_phone']
        contact.fax = request.form['fax']
        contact.email = request.form['email']
        contact.work_email = request.form['work_email']
        contact.home_street = request.form['home_street']
        contact.home_city = request.form['home_city']
        contact.home_state = request.form['home_state']
        contact.home_postal_code = request.form['home_postal_code']
        contact.home_country = request.form['home_country']
        contact.work_street = request.form['work_street']
        contact.work_city = request.form['work_city']
        contact.work_state = request.form['work_state']
        contact.work_postal_code = request.form['work_postal_code']
        contact.work_country = request.form['work_country']
        contact.organization = request.form['organization']
        contact.title = request.form['title']
        contact.role = request.form['role']
        contact.url = request.form['url']
        contact.work_url = request.form['work_url']
        contact.twitter = request.form['twitter']
        contact.linkedin = request.form['linkedin']
        contact.birthday = request.form['birthday']
        contact.anniversary = request.form['anniversary']
        contact.note = request.form['note']
        contact.latitude = request.form['latitude']
        contact.longitude = request.form['longitude']
        db.session.commit()
        return redirect(url_for('index'))
    
    qr_code = generate_contact_qr(contact)
    return render_template('edit.html', contact=contact, qr_code=qr_code)

@app.route('/view/<int:id>')
def view_qr(id):
    contact = Contact.query.get_or_404(id)
    qr_code = generate_contact_qr(contact)
    return render_template('view_qr.html', contact=contact, qr_code=qr_code)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
