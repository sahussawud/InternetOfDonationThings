# InternetOfDonationThings

<li> 🏠 หน้าแรก </li>
<br>
<img src="image/home-1.PNG" width="800px" style="max-width:100%;">
<img src="image/home-2.PNG" width="800px" style="max-width:100%;">
<img src="image/login.PNG" width="800px" style="max-width:100%;">
<img src="image/register-1.PNG" width="800px" style="max-width:100%;">
<img src="image/register-2.PNG" width="800px" style="max-width:100%;">
<img src="image/register-3.PNG" width="800px" style="max-width:100%;">
<img src="image/register-4.PNG" width="800px" style="max-width:100%;">
<img src="image/register-5.PNG" width="800px" style="max-width:100%;">

สำหรับหน้าแรก จะมีโครงการที่กำลังรอรับความช่วยเหลือแต่ละโครงการแสดงอยู่ สามารถเลือกดูและทำการบริจาคได้ แต่จะต้อง Login เข้าสู่ระบบ เพื่อทำการบริจาคหรือรับบริจาคสิ่งของ
กรณีที่ยังไม่ได้ลงทะเบียนเข้าสู่ระบบ ให้กดไปที่ Register จะมีหน้า Register Step 1 ขึ้นมาจากนั้นกรอกข้อมูลลงไป
เมื่อกรอกข้อมูลเสร็จ กด Next จะมีหน้า Register Step 2 ให้เลือกระหว่าง Donor(ผู้บริจาค) หรือ Recipient(ผู้รับบริจาค)

1) สำหรับ Donor(ผู้บริจาค) ให้กรอกข้อมูลส่วนตัว ก็จะเป็นการเสร็จสิ้นการลงทะเบียน
2) สำหรับ Recipient(ผู้รับบริจาค) จะมีให้เลือกระหว่าง Organization(องค์กร) หรือ Person(บุคคลธรรมดา) ทำการเลือกอย่างใดอย่างหนึ่ง และกรอกข้อมูล ก็จะเป็นการเสร็จสิ้นการลงทะเบียน

<li> 📍 Track donations </li>
หน้าแสดงจุดพิกัดของโครงการรับบริจาคสิ่งของ สามารถกดที่กล่องสี่เหลี่ยมด้านขวาบน เพื่อทำการเลือกประเภทของสิ่งของที่รับบริจาคอยู่ได้ และสามารถเลือกดูแผนที่ในรูปแบบต่างๆได้

<li> 🎁 My Donations </li>
หน้าสำหรับ Donor(ผู้บริจาค) จะแสดงสิ่งของที่ผู้บริจาคได้ลงทะเบียนไว้ในหน้า 📠 ลงทะเบียนของ และมีสถานะแสดงว่าได้บริจาคแล้ว หรือ รอการบริจาค เมื่อผู้บริจาคสิ่งของต้องการบริจาคสิ่งของให้กดปุ่มบริจาคเลย ในสิ่งของนั้น ก็จะไปที่หน้าโครงการที่รับของบริจาคตามประเภทที่ได้ลงทะเบียนของไว้ เมื่อเลือกโครงการแล้วกดบริจาคก็เสร็จสิ้นการบริจาคสิ่งของ และสิ่งของนั้นก็จะขึ้นสถานะเป็น บริจาคแล้ว

-สำหรับสิ่งของที่ลงทะเบียนไว้ สามารถติดตามสิ่งของเหล่านั้นได้ โดยกดปุ่มติดตามที่สิ่งของนั้น ก็จะมาที่หน้าการติดตาม โดยจะมี QR Code ในการติดตามสิ่งของ

*** หน้าการตอบกลับ feed back ไปให้ผู้บริจาค สามารถตอบกลับได้โดยการสแกน QR Code ที่ได้ผูกไว้กับสิ่งของชิ้นนั้น เมื่อสแกนเสร็จก็สามารถเขียนข้อความส่งกลับไปยังผู้รับบริจาคได้

<li> 📝 My Project </li>
หน้าสำหรับ Recipient(ผู้รับบริจาค) ที่ใช้สำหรับแสดงรายละเอียดโครงการต่างๆที่ผู้รับริจาคได้สร้างไว้ในหน้า ✏️ สร้างโครงการรับบริจาค สามารถกดปุ่ม รายละเอียด เพื่อดูรายละเอียดโครงการเพิ่มเติมได้

<li> 📠 ลงทะเบียนของ </li>
หน้าสำหรับ Donor(ผู้บริจาค) ใช้สำหรับลงทะเบียนสิ่งของที่ต้องการบริจาค เมื่อกรอกข้อมูลครบแล้วจะไปที่หน้า 🎁 My Donations เพื่อแสดงรายการสิ่งของที่ลงทะเบียนไว้ทั้งหมด

<li> ✏️ สร้างโครงการรับบริจาค </li>
หน้าสำหรับ Recipient(ผู้รับบริจาค) ที่ใช้สำหรับสร้างโครงการรับบริจาคต่างๆ เมื่อกรอกข้อมูลโครงการและกดปุ่มสร้างเสร็จแล้ว สามารถมาดูรายละเอียดโครงการทั้งหมดที่ได้สร้างไว้ได้ที่หน้า My Project

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

## Group Members

|<img src="image/member_1.jpg" width="120px" height="120px">|<img src="image/member_2.jpg" width="120px" height="120px">|<img src="image/member_3.jpg" width="120px" height="120px">|<img src="image/member_4.jpg" width="120px" height="120px">|
|:---:|:---:|:---:|:---:|
|[ongsuwannoo](https://github.com/ongsuwannoo)|[Chokcolate](https://github.com/Chokcolate)|[kenso11](https://github.com/kenso11)|[sahussawud](https://github.com/sahussawud)|
|จักรพรรดิ์<br>สุวรรณโณ|ธีรวัต<br>กาญจนปานวงษ์|ศิรพัชร<br>นาคะรัตนากร|สหัสวรรษ<br>ขันรักษา|
|61070022|61070093|61070219|61070238|
