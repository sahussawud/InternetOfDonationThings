# InternetOfDonationThings

<li>หน้าแรก</li>
Login เข้าสู่ระบบ เพื่อทำการบริจาคหรือรับบริจาคสิ่งของ
กรณีที่ยังไม่ได้ลงทะเบียนเข้าสู่ระบบ ให้กดไปที่ Register จะมีหน้า Register Step 1 ขึ้นมาจากนั้นกรอกข้อมูลลงไป
เมื่อกรอกข้อมูลเสร็จ กด Next จะมีหน้า Register Step 2 ให้เลือกระหว่าง Donor(ผู้บริจาค) หรือ Recipient(ผู้รับบริจาค)

1) สำหรับ Donor(ผู้บริจาค) ให้กรอกข้อมูลส่วนตัว ก็จะเป็นการเสร็จสิ้นการลงทะเบียน
2) สำหรับ Recipient(ผู้รับบริจาค) จะมีให้เลือกระหว่าง Organization(องค์กร) หรือ Person(บุคคลธรรมดา) ทำการเลือกอย่างใดอย่างหนึ่ง และกรอกข้อมูล ก็จะเป็นการเสร็จสิ้นการลงทะเบียน


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
