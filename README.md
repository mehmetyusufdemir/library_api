# Library API / Kütüphane API

This project is a simple Library Management API built with Flask and Oracle Database. It provides endpoints to manage libraries, employees, books, suppliers, and members.

Bu proje, Flask ve Oracle Veritabanı kullanılarak yapılmış basit bir Kütüphane Yönetim API'sidir. API, kütüphaneleri, çalışanları, kitapları, tedarikçileri ve üyeleri yönetmek için uç noktalar sağlar.

## Features / Özellikler

- **Library Management**: Add, update, and delete libraries.
- **Employee Management**: Add, update, and delete employees.
- **Book Management**: Add, update, and delete books.
- **Supplier Management**: Add, update, and delete suppliers.
- **Member Management**: Add, update, and delete members.

- **Kütüphane Yönetimi**: Kütüphaneleri ekleme, güncelleme ve silme.
- **Çalışan Yönetimi**: Çalışanları ekleme, güncelleme ve silme.
- **Kitap Yönetimi**: Kitapları ekleme, güncelleme ve silme.
- **Tedarikçi Yönetimi**: Tedarikçileri ekleme, güncelleme ve silme.
- **Üye Yönetimi**: Üyeleri ekleme, güncelleme ve silme.

## Requirements / Gereksinimler

- Python 3.x
- Flask
- cx_Oracle
- Oracle Database

## Installation / Kurulum

1. Clone the repository / Depoyu klonlayın:
    ```bash
    git clone https://github.com/mehmetyusufdemir/library_api.git
    cd library_api
    ```

2. Install required packages / Gerekli paketleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Oracle Database and configure connection / Oracle Veritabanı'nı kurun ve bağlantıyı yapılandırın.

4. Run the application / Uygulamayı çalıştırın:
    ```bash
    python app.py
    ```

## Endpoints / API Uç Noktaları

### POST /libraries
Add a new library to the system.
Yeni bir kütüphane ekler.

### PUT /libraries/<id>
Update an existing library.
Var olan bir kütüphaneyi günceller.

### DELETE /libraries/<id>
Delete a library.
Bir kütüphaneyi siler.

### POST /employees
Add a new employee to the system.
Yeni bir çalışan ekler.

### PUT /employees/<id>
Update an existing employee.
Var olan bir çalışanı günceller.

### DELETE /employees/<id>
Delete an employee.
Bir çalışanı siler.

### POST /books
Add a new book to the system.
Yeni bir kitap ekler.

### PUT /books/<id>
Update an existing book.
Var olan bir kitabı günceller.

### DELETE /books/<id>
Delete a book.
Bir kitabı siler.

### POST /suppliers
Add a new supplier to the system.
Yeni bir tedarikçi ekler.

### PUT /suppliers/<id>
Update an existing supplier.
Var olan bir tedarikçiyi günceller.

### DELETE /suppliers/<id>
Delete a supplier.
Bir tedarikçiyi siler.

### POST /members
Add a new member to the system.
Yeni bir üye ekler.

### PUT /members/<id>
Update an existing member.
Var olan bir üyeyi günceller.

### DELETE /members/<id>
Delete a member.
Bir üyeyi siler.

## License / Lisans

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Contact / İletişim

- GitHub: [https://github.com/mehmetyusufdemir](https://github.com/mehmetyusufdemir)
- Email: [yusufdem0234@gmail.com](mailto:yusufdem0234@gmail.com)
