# Kullanım Talimatları

Bu projeyi çalıştırmak ve gerekli yapılandırmaları yapmak için aşağıdaki adımları takip edebilirsiniz:

## 1. Migrasyon İşlemlerini Tamamlayın

Projeyi ilk kez çalıştırmadan önce veritabanını hazırlamak için aşağıdaki komutu çalıştırın:

```bash
python manage.py migrate
```

Bu komut, projede tanımlı veritabanı tablolarını oluşturacaktır.

---

## 2. Süper Kullanıcı (Superuser) Oluşturun

Yönetici paneline erişim sağlayabilmek için bir süper kullanıcı oluşturun:

```bash
python manage.py createsuperuser
```

Komut sonrası, kullanıcı adı, e-posta ve şifre bilgilerini girerek süper kullanıcı hesabınızı oluşturabilirsiniz.

---

## 3. Süper Kullanıcıyı "Manager" Rolüne Atayın

Yönetici paneline (admin sayfası) giriş yapın:

- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Süper kullanıcı bilgileriyle giriş yapın.

Süper kullanıcının kullanıcı profiline giderek **"Role"** alanını **"Manager"** olarak güncelleyin.

---

## 4. "Employee" Rolünde Kullanıcı Oluşturun

Yönetici panelinden yeni bir kullanıcı oluşturun ve **"Role"** değerini **"Employee"** olarak atayın.

---

## 5. Giriş Yapın

Yeni oluşturulan kullanıcı bilgilerini kullanarak aşağıdaki giriş sayfasından sisteme giriş yapabilirsiniz:

- **URL:** [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)

Giriş yaptıktan sonra sisteme erişim sağlayabilirsiniz.