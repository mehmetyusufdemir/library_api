from flask import Flask, jsonify,request
import cx_Oracle
from datetime import datetime

app = Flask(__name__)

# Oracle bağlantı bilgileri
try:
    oracle_conn = cx_Oracle.connect("system", "oracle123", "localhost:1521/ORCLPDB1")
    print("Oracle bağlantısı başarılı!")
except cx_Oracle.DatabaseError as e:
    print(f"Oracle bağlantı hatası: {e}")


@app.route('/library', methods=['GET'])
def get_libraries():
    cursor = oracle_conn.cursor()
    query="SELECT * FROM LIBRARIES"
    cursor.execute(query)
    libraries = cursor.fetchall()
    cursor.close()

    library_list = []
    for library in libraries:
        library_list.append({
            'Library_ID': library[0],
            'Library_Name': library[1],
            'Location': library[2],
            'Established_Year': library[3]
        })
    return jsonify(library_list)


@app.route('/libraries/country', methods=['GET'])
def get_libraries_by_country():
    cursor = oracle_conn.cursor()
    query = "SELECT * FROM LIBRARIES WHERE Location = 'Los Angeles'"  # Şehir filtresi
    cursor.execute(query)
    libraries = cursor.fetchall()
    cursor.close()

    library_list = []
    for library in libraries:
        library_list.append({
            'Library_ID': library[0],
            'Library_Name': library[1],
            'Location': library[2],
            'Established_Year': library[3]
        })
    return jsonify(library_list)


@app.route('/employees', methods=['GET'])
def get_employees():
    cursor = oracle_conn.cursor()
    query = "SELECT * FROM EMPLOYEES"
    cursor.execute(query)
    employees = cursor.fetchall()
    cursor.close()

    employee_list = []
    for employee in employees:
        employee_list.append({
            'Employee_ID': employee[0],
            'First_Name': employee[1],
            'Last_Name': employee[2],
            'Job_Title': employee[3],
            'Salary': employee[4],
            'Hire_Date': employee[5],
            'Library_ID': employee[6]
        })
    return jsonify(employee_list)


@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    cursor = oracle_conn.cursor()
    query = "SELECT * FROM SUPPLIERS"
    cursor.execute(query)
    suppliers = cursor.fetchall()
    cursor.close()

    supplier_list = []
    for supplier in suppliers:
        supplier_list.append({
            'Supplier_ID': supplier[0],
            'Supplier_Name': supplier[1],
            'Contact_Person': supplier[2],
            'Phone_Number': supplier[3],
            'Email': supplier[4]
        })
    return jsonify(supplier_list)

################################################
# POST: Yeni Kütüphane Ekle
@app.route('/libraries', methods=['POST'])
def add_library():
    try:
        data = request.get_json()
        library_name = data['Library_Name']
        location = data['Location']
        established_year = data['Established_Year']

        # Oracle bağlantısı ile cursor oluşturuluyor
        cursor = oracle_conn.cursor()

        # En yüksek Library_ID'yi alıyoruz
        cursor.execute("SELECT MAX(Library_ID) FROM Libraries")
        max_library_id = cursor.fetchone()[0]  # max_library_id en yüksek değeri alacak

        # Eğer en yüksek ID null ise (yani tablo boşsa), 1'den başlatıyoruz
        if max_library_id is None:
            new_library_id = 1
        else:
            new_library_id = max_library_id + 1  # Yeni Library_ID, en yüksek ID + 1 olacak

        # Veriyi tabloya ekliyoruz
        query = "INSERT INTO Libraries (Library_ID, Library_Name, Location, Established_Year) VALUES (:new_library_id, :library_name, :location, :established_year)"
        cursor.execute(query, new_library_id=new_library_id, library_name=library_name, location=location, established_year=established_year)

        # Değişiklikleri kaydediyoruz
        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Kütüphane başarıyla eklendi!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# POST: Yeni Çalışan Ekle
@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        first_name = data['First_Name']
        last_name = data['Last_Name']
        job_title = data['Job_Title']
        salary = data['Salary']
        hire_date = data['Hire_Date']
        library_id = data['Library_ID']

        # Tarih formatını doğru hale getirme (YYYY-MM-DD)
        hire_date_obj = datetime.strptime(hire_date, "%Y-%m-%d").date()

        cursor = oracle_conn.cursor()

        # En yüksek Employee_ID'yi alıyoruz
        cursor.execute("SELECT MAX(Employee_ID) FROM EMPLOYEES")
        max_employee_id = cursor.fetchone()[0]  # max_employee_id en yüksek değeri alacak

        # Eğer en yüksek ID null ise (yani tablo boşsa), 1'den başlatıyoruz
        if max_employee_id is None:
            new_employee_id = 1
        else:
            new_employee_id = max_employee_id + 1  # Yeni Employee_ID, en yüksek ID + 1 olacak

        query = """
        INSERT INTO EMPLOYEES (Employee_ID, First_Name, Last_Name, Job_Title, Salary, Hire_Date, Library_ID)
        VALUES (:employee_id, :first_name, :last_name, :job_title, :salary, :hire_date, :library_id)
        """
        cursor.execute(query, employee_id=new_employee_id, first_name=first_name, last_name=last_name,
                       job_title=job_title, salary=salary, hire_date=hire_date_obj, library_id=library_id)
        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Çalışan başarıyla eklendi!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# POST: Yeni Tedarikçi Ekle
@app.route('/suppliers', methods=['POST'])
def add_supplier():
    try:
        data = request.get_json()
        supplier_name = data['Supplier_Name']
        contact_person = data['Contact_Person']
        phone_number = data['Phone_Number']
        email = data['Email']

        cursor = oracle_conn.cursor()

        # En yüksek Supplier_ID'yi alıyoruz
        cursor.execute("SELECT MAX(Supplier_ID) FROM SUPPLIERS")
        max_supplier_id = cursor.fetchone()[0]

        # Eğer en yüksek ID null ise (yani tablo boşsa), 1'den başlatıyoruz
        if max_supplier_id is None:
            new_supplier_id = 1
        else:
            new_supplier_id = max_supplier_id + 1  # Yeni Supplier_ID, en yüksek ID + 1 olacak

        # Veriyi tabloya ekliyoruz
        query = """
        INSERT INTO SUPPLIERS (Supplier_ID, Supplier_Name, Contact_Person, Phone_Number, Email)
        VALUES (:new_supplier_id, :supplier_name, :contact_person, :phone_number, :email)
        """
        cursor.execute(query, new_supplier_id=new_supplier_id, supplier_name=supplier_name,
                       contact_person=contact_person, phone_number=phone_number, email=email)
        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Tedarikçi başarıyla eklendi!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


#POST: kitap ekleme
@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        title = data['Title']
        author = data['Author']
        isbn = data['ISBN']
        published_year = data['Published_Year']
        category_id = data['Category_ID']
        library_id = data['Library_ID']
        available_copies = data['Available_Copies']

        cursor = oracle_conn.cursor()

        # En yüksek Book_ID'yi alıyoruz
        cursor.execute("SELECT MAX(Book_ID) FROM BOOKS")
        max_book_id = cursor.fetchone()[0]

        # Eğer en yüksek ID null ise (yani tablo boşsa), 1'den başlatıyoruz
        if max_book_id is None:
            new_book_id = 1
        else:
            new_book_id = max_book_id + 1  # Yeni Book_ID, en yüksek ID + 1 olacak

        # Veriyi tabloya ekliyoruz
        query = """
        INSERT INTO BOOKS (Book_ID, Title, Author, ISBN, Published_Year, Category_ID, Library_ID, Available_Copies)
        VALUES (:new_book_id, :title, :author, :isbn, :published_year, :category_id, :library_id, :available_copies)
        """
        cursor.execute(query, new_book_id=new_book_id, title=title, author=author, isbn=isbn,
                       published_year=published_year, category_id=category_id, library_id=library_id,
                       available_copies=available_copies)
        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Kitap başarıyla eklendi!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# POST: Yeni Üye Ekle
@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        first_name = data['First_Name']
        last_name = data['Last_Name']
        email = data['Email']
        phone_number = data['Phone_Number']
        join_date = data['Join_Date']
        library_id = data['Library_ID']

        # 📌 Tarih formatını Oracle'ın anlayacağı forma çeviriyoruz
        join_date_obj = datetime.strptime(join_date, "%Y-%m-%d").date()

        cursor = oracle_conn.cursor()

        # 📌 Yeni Member_ID'yi belirlemek için mevcut en büyük ID'yi al
        cursor.execute("SELECT NVL(MAX(Member_ID), 0) + 1 FROM MEMBERS")
        new_member_id = cursor.fetchone()[0]

        query = """
        INSERT INTO MEMBERS (Member_ID, First_Name, Last_Name, Email, Phone_Number, Join_Date, Library_ID)
        VALUES (:member_id, :first_name, :last_name, :email, :phone_number, TO_DATE(:join_date, 'YYYY-MM-DD'), :library_id)
        """
        cursor.execute(query, member_id=new_member_id, first_name=first_name, last_name=last_name, email=email,
                       phone_number=phone_number, join_date=join_date_obj, library_id=library_id)
        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": f"Üye başarıyla eklendi! ID: {new_member_id}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
###################################################################

#ders sorgu 1 belli bir lokasyonda kiralanmış kitapların aylık olarak adetleri
@app.route('/issued-books/monthly', methods=['POST'])
def get_monthly_issued_books():
    try:
        data = request.get_json()
        location = data.get('location')  # JSON içinden lokasyonu al

        if not location:
            return jsonify({"error": "Lütfen bir lokasyon belirtin."}), 400

        cursor = oracle_conn.cursor()
        query = """
        SELECT 
            TO_CHAR(BI.ISSUE_DATE, 'YYYY-MM') AS ISSUE_MONTH,
            COUNT(BI.BOOK_ID) AS TOTAL_ISSUED_BOOKS,
            BC.CATEGORY_NAME,  
            M.FIRST_NAME || ' ' || M.LAST_NAME AS MEMBER_NAME
        FROM BOOKS_ISSUED BI
        JOIN BOOKS B ON BI.BOOK_ID = B.BOOK_ID  
        JOIN LIBRARIES L ON B.LIBRARY_ID = L.LIBRARY_ID  
        JOIN MEMBERS M ON BI.MEMBER_ID = M.MEMBER_ID  
        JOIN BOOK_CATEGORIES BC ON B.CATEGORY_ID = BC.CATEGORY_ID  
        WHERE L.LOCATION = :location  
        GROUP BY TO_CHAR(BI.ISSUE_DATE, 'YYYY-MM'), BC.CATEGORY_NAME, M.FIRST_NAME, M.LAST_NAME
        ORDER BY TO_CHAR(BI.ISSUE_DATE, 'YYYY-MM')
        """

        cursor.execute(query, {"location": location})
        result = cursor.fetchall()
        cursor.close()

        issued_books = [
            {
                "issue_month": row[0],
                "total_issued_books": row[1],
                "category_name": row[2],
                "member_name": row[3]
            }
            for row in result
        ]

        return jsonify(issued_books), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#sorgu 2 kiralanmış kitapların kaç defa kiralandığı ve mevcut kitap sayısı
@app.route('/book-borrowing-stats', methods=['GET'])
def get_book_borrowing_stats():
    try:
        cursor = oracle_conn.cursor()

        # SQL Sorgusu
        query = """
        SELECT 
            B.BOOK_ID,
            B.TITLE,
            L.LIBRARY_NAME,
            COUNT(BI.BOOK_ID) AS TOTAL_BORROWED,  -- Kaç kez ödünç alınmış
            B.AVAILABLE_COPIES - 
            COALESCE(SUM(CASE WHEN BI.RETURN_DATE IS NOT NULL THEN 1 ELSE 0 END), 0) AS CURRENT_STOCK  -- Gerçek stok
        FROM BOOKS B
        LEFT JOIN BOOKS_ISSUED BI ON B.BOOK_ID = BI.BOOK_ID  -- Kitap kiralama bilgilerini alıyoruz
        JOIN LIBRARIES L ON B.LIBRARY_ID = L.LIBRARY_ID  -- Kütüphane bilgisi
        GROUP BY B.BOOK_ID, B.TITLE, L.LIBRARY_NAME, B.AVAILABLE_COPIES
        ORDER BY TOTAL_BORROWED DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        # Sonuçları JSON formatında döndürüyoruz
        books_data = []
        for row in result:
            books_data.append({
                "BOOK_ID": row[0],
                "TITLE": row[1],
                "LIBRARY_NAME": row[2],
                "TOTAL_BORROWED": row[3],
                "CURRENT_STOCK": row[4]
            })

        return jsonify(books_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
##########################################################################
#güncelleme işlemleri
@app.route('/libraries/<int:library_id>', methods=['PUT'])
def update_library(library_id):
    try:
        data = request.get_json()
        library_name = data['Library_Name']
        location = data['Location']
        established_year = data['Established_Year']

        cursor = oracle_conn.cursor()

        # Kütüphaneyi güncelleme
        query = """
        UPDATE LIBRARIES
        SET Library_Name = :library_name, Location = :location, Established_Year = :established_year
        WHERE Library_ID = :library_id
        """
        cursor.execute(query, library_id=library_id, library_name=library_name, location=location, established_year=established_year)

        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Kütüphane başarıyla güncellendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        first_name = data['First_Name']
        last_name = data['Last_Name']
        job_title = data['Job_Title']
        salary = data['Salary']
        hire_date = data['Hire_Date']
        library_id = data['Library_ID']

        # Tarih formatını doğru hale getirme (YYYY-MM-DD)
        hire_date_obj = datetime.strptime(hire_date, "%Y-%m-%d").date()

        cursor = oracle_conn.cursor()

        # Çalışanı güncelleme
        query = """
        UPDATE EMPLOYEES
        SET First_Name = :first_name, Last_Name = :last_name, Job_Title = :job_title,
            Salary = :salary, Hire_Date = :hire_date, Library_ID = :library_id
        WHERE Employee_ID = :employee_id
        """
        cursor.execute(query, employee_id=employee_id, first_name=first_name, last_name=last_name,
                       job_title=job_title, salary=salary, hire_date=hire_date_obj, library_id=library_id)

        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Çalışan başarıyla güncellendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    try:
        data = request.get_json()
        supplier_name = data['Supplier_Name']
        contact_person = data['Contact_Person']
        phone_number = data['Phone_Number']
        email = data['Email']

        cursor = oracle_conn.cursor()

        # Tedarikçiyi güncelleme
        query = """
        UPDATE SUPPLIERS
        SET Supplier_Name = :supplier_name, Contact_Person = :contact_person,
            Phone_Number = :phone_number, Email = :email
        WHERE Supplier_ID = :supplier_id
        """
        cursor.execute(query, supplier_id=supplier_id, supplier_name=supplier_name, contact_person=contact_person,
                       phone_number=phone_number, email=email)

        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Tedarikçi başarıyla güncellendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        data = request.get_json()
        title = data['Title']
        author = data['Author']
        isbn = data['ISBN']
        published_year = data['Published_Year']
        category_id = data['Category_ID']
        library_id = data['Library_ID']
        available_copies = data['Available_Copies']

        cursor = oracle_conn.cursor()

        # Kitabı güncelleme
        query = """
        UPDATE BOOKS
        SET Title = :title, Author = :author, ISBN = :isbn, Published_Year = :published_year,
            Category_ID = :category_id, Library_ID = :library_id, Available_Copies = :available_copies
        WHERE Book_ID = :book_id
        """
        cursor.execute(query, book_id=book_id, title=title, author=author, isbn=isbn, published_year=published_year,
                       category_id=category_id, library_id=library_id, available_copies=available_copies)

        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Kitap başarıyla güncellendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        data = request.get_json()
        first_name = data['First_Name']
        last_name = data['Last_Name']
        email = data['Email']
        phone_number = data['Phone_Number']
        membership_date = data['Membership_Date']
        library_id = data['Library_ID']

        # Tarih formatını doğru hale getirme (YYYY-MM-DD)
        membership_date_obj = datetime.strptime(membership_date, "%Y-%m-%d").date()

        cursor = oracle_conn.cursor()

        # Üyeyi güncelleme
        query = """
        UPDATE MEMBERS
        SET First_Name = :first_name, Last_Name = :last_name, Email = :email,
            Phone_Number = :phone_number, Membership_Date = :membership_date, Library_ID = :library_id
        WHERE Member_ID = :member_id
        """
        cursor.execute(query, member_id=member_id, first_name=first_name, last_name=last_name, email=email,
                       phone_number=phone_number, membership_date=membership_date_obj, library_id=library_id)

        oracle_conn.commit()
        cursor.close()

        return jsonify({"message": "Üye başarıyla güncellendi!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)
