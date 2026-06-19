# E-Commerce Backend API

## Özet

Bu repository, Django ve Django REST Framework ile geliştirilen bir e-commerce backend çalışmasını içermektedir. Proje, başlangıçta bir kurs kapsamında geliştirilen temel bir uygulamayı esas almakta; sonrasında ise bu yapı, daha modüler ve daha gerçekçi backend ihtiyaçlarını karşılayacak şekilde genişletilmektedir.

Bu nedenle çalışma, tamamlanmış bir ürün olmaktan çok, mevcut bir e-commerce çekirdeğinin mimari olarak nasıl ileri taşındığını gösteren bir backend geliştirme pratiği olarak değerlendirilmelidir.

## Teknik Odak

Bu repo, özellikle aşağıdaki alanlarda yapılan geliştirmeleri görünür kılmaktadır:

- iş kurallarının view katmanından ayrıştırılarak service layer yaklaşımına taşınması
- kullanıcı yaşam döngüsünün login ile sınırlı bırakılmayıp email verification ve password reset akışlarıyla genişletilmesi
- email gönderiminin Celery üzerinden asenkron hale getirilmesi
- sepet, adres, kupon, sipariş ve ödeme süreçlerinin tek bir checkout hattında birleştirilmesi
- transaction yönetimi ile sipariş akışında veri bütünlüğünün korunmaya çalışılması
- iyzico entegrasyonunun doğrudan sipariş sürecine bağlanması
- OpenAPI tabanlı dokümantasyon ve Docker tabanlı çalışma altyapısının eklenmesi

## Mimari Yaklaşım

Kod tabanı, yalnızca endpoint üreten bir yapı olarak değil, katmanlı bir backend düzeni içinde ele alınmıştır. Bu yapıda:

- `views` HTTP katmanını
- `serializers` veri doğrulama ve dönüşümünü
- `services` iş kurallarını
- `models` kalıcılık ve veri ilişkilerini

üstlenmektedir.

Bu ayrım özellikle sipariş oluşturma, stok kontrolü, kupon doğrulama, adres sahipliği kontrolü, email token üretimi ve ödeme entegrasyonu gibi alanlarda belirgindir.

## Öne Çıkan Teknik Katkılar

### Service Layer ve iş kuralı ayrıştırması

Projede önemli iş akışları doğrudan view içine yazılmamış; servis fonksiyonlarına taşınmıştır. Bu tercih, kodun bakımını kolaylaştırmakta ve sipariş, sepet, kupon, adres ve kullanıcı işlemlerinde daha okunabilir bir iş akışı oluşturmaktadır.

### Hesap yaşam döngüsü

Authentication yapısı yalnızca JWT login ile sınırlı değildir. Email tabanlı kullanıcı modeli, email verification, password reset, token üretimi ve kullanıcı varlığını doğrudan ifşa etmeyen response yaklaşımı birlikte ele alınmıştır.

### Asenkron email işleme

Password reset ve email verification mailleri request-response akışından ayrıştırılarak Celery görevleri üzerinden arka planda işlenecek şekilde kurgulanmıştır. Bu, email gönderiminin yalnızca ek bir özellik değil, mimari bir tercih olarak ele alındığını göstermektedir.

### Checkout orkestrasyonu

Teknik yoğunluğun en yüksek olduğu alan checkout akışıdır. Sepet içeriğinin okunması, adreslerin doğrulanması, kupon uygulanması, sipariş kalemlerinin üretilmesi, ödeme sürecinin başlatılması ve bazı sipariş sonrası görevlerin kuyruğa bırakılması aynı iş hattında toplanmıştır.

### Ödeme entegrasyonu

iyzico entegrasyonu bağımsız bir deneme olarak değil, sipariş akışının parçası olarak ele alınmıştır. Sipariş verisinin ödeme sağlayıcısının beklediği formata dönüştürülmesi ve hata kodlarının anlamlı mesajlara çevrilmesi bu katmanın temel katkıları arasındadır.

## Teknoloji Yığını

- Python
- Django 5
- Django REST Framework
- Simple JWT
- Celery
- Redis
- drf-spectacular
- django-filter
- iyzico / iyzipay
- Docker

## Mevcut Durum

Bu proje aktif olarak geliştirilmektedir; tamamlanmış ve production-ready bir ürün olarak değerlendirilmemelidir. Buna karşılık mevcut haliyle, bir kurs projesi temel alınarak daha güçlü backend pratikleriyle nasıl genişletilebileceğini açık biçimde göstermektedir.

Mevcut sınırlar kısaca şöyledir:

- otomatik test kapsamı henüz oluşmamıştır
- geliştirme ortamında SQLite kullanılmaktadır
- security hardening, observability ve CI/CD gibi alanlar sonraki iterasyonlara açıktır

## Sonuç

Bu repository’nin temel değeri, çok sayıda modül içermesi değil; kullanıcı yönetimi, email akışları, checkout orkestrasyonu, ödeme entegrasyonu ve iş kuralı ayrıştırmasını aynı backend içinde bir araya getirmesidir.

Bu yönüyle repo, bir kurs projesinin ötesine geçerek mevcut bir kod tabanının daha sistematik ve daha sürdürülebilir bir backend mimarisine doğru nasıl geliştirildiğini göstermektedir.
