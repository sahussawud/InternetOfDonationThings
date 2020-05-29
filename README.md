# InternetOfDonationThings

<li>หน้าแรก</li>
Login เข้าสู่ระบบ เพื่อทำการบริจาคสิ่งของ
กรณีที่ยังไม่ได้ลงทะเบียนเข้าสู่ระบบ ให้กดไปที่ Registrr จะมีหน้า Registrr Step 1 ขึ้นมาจากนั้นกรอกข้อมูลลงไป
เมื่อกรอกข้อมูลเสร็จ กด Next จะมีหน้า Registrr Step 2 ให้เลือกระหว่าง Donor (ผู้บริจาค) หรือ Recipient (ผู้รับบริจาค)


This Project from ITKMITL

```
python -m venv env
```

Select Interpreter ``ctrl + shift + P``

```
'env':venv
```

OR

```
/env/Scripts/Activate.ps1
```

Install Requirements files
```
pip install -r requirements.txt
```
Create or Update Database
```
python manage.py makemigrations
python manage.py migrate
```

Runserver !
```
python .\manage.py runserver
```
