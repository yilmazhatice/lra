# Bir Aylık Proje Planı: Microsoft **Foundry Local** ile **Lokal RAG** Yapay Zeka Asistanı **Man link: https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-your-first-local-rag-application-with-foundry-local/4501968**

![./media/image1.png](./media/image1.png)

Hedef, **başlangıç seviyesindeki bilgisayar bilimleri öğrencilerine,
*çevrimdışı model çıkarımı (inference) için Microsoft Foundry Local'i ve
RAG (Retrieval-Augmented Generation) mimarisini kullanarak yerel bir
soru-cevap/bilgi asistanı oluşturdukları tam zamanlı, bir aylık bir yaz
programı boyunca rehberlik etmektir. Nihai proje, belgelerden gelen soruları
sıfır internet bağımlılığı ile yanıtlayan yerel bir RAG destek temsilcisinin
Microsoft Tech Community örneğinden esinlenmiştir. Programın sonunda, her
öğrenci ekibi, yerel olarak bilgi alarak ve bunu büyük bir dil modelinin (LLM)
yanıtlarına entegre ederek küçük bir belge koleksiyonu (örneğin ders notları,
kılavuzlar, SSS'ler) hakkında soruları yanıtlayabilen çalışan bir çevrimdışı
soru-cevap sohbet robotuna (chatbot) sahip olacaktır.
[\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)***

**Program Yapısı:** Ayı, her biri belirli becerilere ve çıktılara odaklanan
üç aşamaya (phase) ayırıyoruz:

-   **Phase 1 -- Temel Öğrenim (1-2. Haftalar):** RAG kavramlarına,
    Foundry Local'a, embeddings (vektör temsilleri), vector search (vektör
    araması), SQLite ve prompt engineering (istem mühendisliği)
    temellerine giriş.

-   **Phase 2 -- Proje Uygulaması (3-4. Haftalar):** Veri alımından (data
    ingestion) ve getirme boru hattından (retrieval pipeline), cihaz
    üzerindeki LLM (Büyük Dil Modeli) ile uygulama entegrasyonuna kadar
    RAG uygulamasının pratik geliştirilmesi.

-   **Phase 3 -- Test ve Dokümantasyon (5. Hafta ve isteğe bağlı olarak 6.
    Hafta):** Sistem testi ve değerlendirmesi, performans ince ayarı (tuning)
    ve proje dokümantasyonu ile nihai sunumların hazırlanması.

Aşağıda, her aşama öğrenme hedefleri, kaynaklar, **pratik egzersizler (hands-on)**,
ve **kilometre taşları (milestones)** ile haftalara göre ayrılmıştır. Program
esnektir (destekleyici öğrenme için bazı konular haftalar arasında çakışabilir).
**Resmi Microsoft kaynakları ve yüksek kaliteli öğreticiler (tutorials)** her
konu için sağlanmıştır. (Topluluk blog kaynakları buna göre belirtilmiştir.)

## **Proje Genel Bakışı & Temel Teknolojiler**

Haftalık plana dalmadan önce, **projeyi ve bileşenlerini** netleştirelim:

-   **Proje Amacı:** Tamamen öğrencinin bilgisayarında çalışan basit bir sohbet
    robotu (chatbot) olan **yerel bir belge soru-cevap asistanı** oluşturmak.
    Cevap üretimi için *yerel bir belge bilgi tabanından (knowledge base)
    ilgili içeriği getirerek bunu yerel bir LLM'e beslemek* için
    **Retrieval-Augmented Generation (RAG)** kullanır. Bu, **daha az
    halüsinasyon (uydurma) ve daha doğru, kaynağa dayalı cevaplar** ile
    sonuçlanır. Asistan, *cihaz üzerinde çalışan bir LLM çalışma zamanı
    (runtime)* sağlayan **Microsoft Foundry Local** aracılığıyla
    çevrimdışı (internet gerektirmeden) çalışabilir.
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

-   **Foundry Local:** *Nedir?* Foundry Local, büyük dil modellerini tamamen
    *kullanıcının cihazında* çalıştırmak için hafif bir çalışma zamanı (runtime)
    ve SDK sağlayan, optimize edilmiş modellerden oluşan küratörlü bir
    katalog içeren **uçtan uca yerel bir yapay zeka çözümüdür**. **Bulut hesabı
    veya GPU gerekmez** -- Foundry Local modelleri otomatik olarak indirir
    ve yönetir, CPU/NPU hızlandırmasıyla çıkarım (inference) yapar; böylece
    uygulamalar **sıfır ağ çağrısıyla yerel, çevrimdışı yapay zeka** sunabilir.
    Bu, öğrencilerin **yerel olarak bir LLM (örneğin daha küçük bir GPT
    varyantı) ile** denemeler yapmasına olanak tanıdığı için projemizin
    anahtarıdır.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local)
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

-   **Retrieval-Augmented Generation (RAG):** RAG, bir belge kümesinden ilgili
    bilgileri getirdiğiniz (**Retrieve**), modelin giriş istemini (prompt) bu
    bilgiyle bağlam olarak zenginleştirdiğiniz (**Augment**) ve ardından modelin
    bir yanıt üretmesini (**Generate**) sağladığınız bir **yapay zeka tasarım
    örüntüsüdür (AI design pattern)**. Böylece modelin yanıtları,
    **embedding tabanlı anlamsal arama (semantic search)** ile bir LLM'i
    birleştirerek *kendi verilerinize dayandırılır* (halüsinasyonu azaltır
    ve kaynak atıfları sağlar). RAG'ın *neden* yararlı olduğunu (özellikle
    özel soru-cevap temsilcileri için) inceleyecek ve bunu daha basit bağlam
    yerleştirme (context injection) yöntemleriyle karşılaştıracağız.
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   **Embeddings & Vektör Araması (Vector Search):** **Text embeddings** (metin
    anlamının sayısal vektör temsilleri) kavramını ve bunları **anlamsal
    benzerlik araması (semantic similarity search)** için nasıl kullanacağımızı
    tanıtacağız. Öğrenciler, RAG'ın genellikle belgeleri bir *vektör
    veritabanında (vector database)* saklamak üzere vektörlere dönüştürmek için
    bir *embedding modeline* nasıl dayandığını ve sorguların nasıl embed
    edilebileceğini ve vektör benzerliğini ölçerek ilgili belgelerle nasıl
    eşleştirilebileceğini öğreneceklerdir. Bunu hem kavramsal olarak hem de
    uygulamada Foundry Local'ın embedding yetenekleriyle göreceğiz.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   **SQLite for Local Data:** Belge metinlerini ve bunların embedding'lerini
    saklamak için hafif bir yerel veritabanı olarak **SQLite** kullanıyoruz.
    SQLite, *sunucusuz, bağımsız (self-contained) bir SQL veritabanıdır* (yalnızca
    tek bir dosya) ve dünyada en yaygın olarak dağıtılan veritabanı motorudur.
    Avantajları arasında *ayrı bir sunucu gerektirmemesi, platformlar arası
    destek sunması ve basit entegrasyonu* yer alır; bu da onu yerel veri
    depolama için ideal kılar. Temel SQL/SQLite kullanımını ele alacağız,
    böylece öğrenciler belgelerini ve vektörlerini yönetmek (örneğin
    *embedding vektörlerini* ve metin parçalarını kaydetmek ve geri getirmek)
    için bunu güvenle kullanabilecekler.
    [\[sqlite.org\]](https://sqlite.org/index.html)
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/apps/develop/data-access/sqlite-data-access)

-   **Prompt Engineering:** Etkili yanıtlar için iyi LLM istemleri (özellikle
    rol talimatları için **sistem istemleri (system prompts)** ve sorgular için
    **kullanıcı istemleri (user prompts)**) hazırlamak hayati önem taşır. Soru-cevap
    görevleri için, modele kaynak göstermesini talimatlandırma ve emin değilse
    yanıt vermemesini söyleme gibi temel **prompt engineering tekniklerini**
    tartışacağız. Öğrenciler basit istemler yazma alıştırması yapacak ve istem
    tasarımının modelin davranışını nasıl etkileyebileceğini anlayacaklar.

-   **Proje Mimarisi:** Nihai uygulama, tüm bileşenlerin tek bir makinede
    bulunduğu basit bir mimariye sahip olacaktır. Bu mimari; bir **istemci
    arayüzü (client interface)** (örneğin, sorular için temel bir web arayüzü
    veya konsol girdisi), kullanıcı sorgularını işleyen ve getirme ile
    üretimi koordine eden bir **sunucu/boru hattı (server/pipeline)** katmanı,
    bir **veri katmanı** (belge embedding'lerini saklayan SQLite veritabanı)
    ve bir **yapay zeka katmanı**ndan (cihaz üzerinde çıkarım yapan Foundry
    Local LLM) oluşur. Aşağıda bu mimarinin görsel bir özeti bulunmaktadır:
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

![./media/image2.png](./media/image2.png) *Şekil 1: Tek bir cihazda Foundry Local
kullanan yerel bir RAG (Retrieval-Augmented Generation) sisteminin mimarisi.
Kullanıcının sorgusu, SQLite vektör veritabanından ilgili belge parçalarını
getiren ("vector search") ve ardından sorguyu artı getirilen bağlamı
("augmented context") Foundry Local SDK'sı aracılığıyla yerel bir LLM'e gönderen
yerel bir uygulama tarafından işlenir. LLM'in yanıtı kullanıcıya döndürülür --
tüm bunlar internet bağlantısı gerekmeden gerçekleşir.*
[\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

![./media/image3.png](./media/image3.png)

[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local),
[\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/),
[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/apps/develop/data-access/sqlite-data-access),
[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)

Yukarıdakiler, öğretime ve kendi kendine çalışmaya rehberlik edecek **temel
konular ve referanslardır**. Bağlam belirlendikten sonra, şimdi **aşama
aşama planı** detaylandırabiliriz:

## **Phase 1 (1-2. Haftalar): Temel Öğrenim**

**Hedefler:** RAG ve yerel yapay zeka araçlarında güçlü bir kavramsal temel
oluşturmak. 2. Haftanın sonunda, öğrenciler **RAG'ın nasıl çalıştığını anlamalı**
ve temel teknolojiler ile geliştirme ortamına aşina olmalıdır. Dizüstü
bilgisayarlarında (hem Windows hem de macOS) **Foundry Local kurulu ve test
edilmiş olacak**, örnek bir **SQLite veritabanı** oluşturulmuş olacak ve belki
de küçük test programları çalıştırılmış olacaktır (embedding üretimi ve vektör
benzerlik araması).

### **1. Hafta:** *RAG Kavramı & Yerel Yapay Zeka Kurulumu*

**Konular & Faaliyetler:**

-   **RAG (Retrieval-Augmented Generation) Giriş:** RAG'ın çözdüğü *sorunu*
    açıklayarak başlayın. Basit örnekler kullanın: genel bir LLM'e belirli bir
    uzmanlık alanıyla ilgili soru sorun (muhtemelen yanlış cevaplayacaktır),
    ardından yanıtları iyileştirmek için RAG'ın dış bilgileri nasıl dahil
    edebileceğini açıklayın. RAG'ın **"retrieve (getir), augment (zenginleştir),
    generate (üret)"** adımlarını ve bunun sonucunda elde edilen faydaları (daha
    doğru yanıtlar, azaltılmış halüsinasyonlar) ele alın.
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

    -   *Kaynak:* *Microsoft Tech Community* blog yazısı *"Building Your First
        Local RAG Application with Foundry Local"* -- anlaşılır bir genel bakış
        için **giriş ve "What is RAG" (RAG Nedir) bölümlerini okuyun** (topluluk
        içeriği).
        [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

    -   *Egzersiz:* **Soru-Cevap rol yapma (role-play):** Kısa bir belge veya
        bilgi tabanı (1 sayfa) sağlayın ve öğrencilerin RAG'ı manuel olarak
        simüle etmesini sağlayın -- biri "retriever" (ilgili paragrafı bulur)
        rolünü oynar, diğeri ise "LLM" (bu bilgiyi kullanarak bir yanıt
        formüle eder) rolünü üstlenir. Bu, bağlam eklemenin soruları
        yanıtlamaya nasıl yardımcı olduğunu gösterir.

-   **Foundry Local'ı Anlama & Ortam Kurulumu:** **Microsoft Foundry Local**'ı
    ve bunun projemiz için neden kilit öneme sahip olduğunu tanıtın.
    Öğrencilerin dizüstü bilgisayarlarında **tamamen çevrimdışı bir LLM**
    çalıştırmaya izin verdiğini vurgulayın (bulut gerekmez) ve desteklenen
    platformlardan (Windows/macOS/Linux) bahsedin. Foundry Local'ın ana
    özelliklerini ele alın: cihaz üzerinde model indirme, donanım hızlandırma
    (CPU/GPU/NPU'yu otomatik kullanma) ve Python (ve diğer diller) için
    kullanımı kolay bir SDK.
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local)

    -   *Kaynak:* Üst düzey bir genel bakış için **Resmi dokümantasyon -- "What
        is Foundry Local?"**. Ayrıca adım adım kurulum talimatları için
        **Microsoft Learn'ün "Get started with Foundry Local" kılavuzuna**
        bakın (*Python* sekmesini seçin).
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/what-is-foundry-local)
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

    -   *Egzersiz:* Her öğrencinin makinesine **Foundry Local SDK**'sını
        (en son sürümünü) yükleyin (hem Windows hem de macOS kurulumlarının
        test edildiğinden emin olun). Pip aracılığıyla yüklemek için resmi
        talimatları izleyin (pip install foundry-local-sdk veya işletim
        sistemine özel varyantı). Kurulumu doğrulamak için bir *"Hello Model"
        testi* çalıştırın: örneğin, Foundry Local SDK'sını kullanarak küçük
        bir modeli (phi-1.5-mini gibi) yükleyen ve basit bir tamamlama üreten
        (örneğin, "Hello, world" istemi verildiğinde selamlamayı tamamlayan)
        kısa bir Python betiği yazın. Bu, çalışma zamanının çalıştığını
        onaylar ve API'yi tanıtır.
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   **Temel Python Uygulama Yapısı:** (Öğrenci geçmişi nedeniyle gerekirse) Bir
    Python projesinin nasıl yapılandırılacağını gözden geçirin: net bir giriş
    noktasına sahip bir main.py kullanmak (if \_\_name\_\_ ==
    \"\_\_main\_\_\": main()), kodun fonksiyonlara veya modüllere bölünmesi
    (proje büyüdükçe netlik sağlamak için) ve bağımlılıkların requirements.txt
    aracılığıyle yönetilmesi. Kodun nasıl organize edileceğini göstermek için
    basit bir örnek (örneğin bir "Hello LLM" projesi) kullanın.

    -   *Kaynak:* **Microsoft Learn --** *"Tutorial: Build a RAG
        application".* *"Prerequisites"* (Önkoşullar) bölümünü ve main.py'yi
        ayarlama ile ilgili kısmı okumaya başlayın. Örnek kod, proje yapımız
        için bir şablon görevi görecektir.
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

    -   *Egzersiz:* **Bir iskelet proje oluşturun:** RAG asistanı için yeni bir
        Python proje klasörü başlatın (initialize). Bir main.py dosyası
        oluşturun ve bir selamlama yazdırarak test edin. VS Code gibi bir kod
        düzenleyici kullanılıyorsa, tüm öğrencilerin programı kendi
        ortamlarında çalıştırabildiğinden emin olun.

**1. Hafta sonundaki Kilometre Taşları (Milestones):** Tüm öğrencilerin
makinelerinde **Foundry Local kurulmuş ve çalışıyor** durumdadır, main.py
dosyası içeren temel bir proje klasörüne sahiptirler ve basit bir Foundry Local
çıkarımı çalıştırabilirler (örneğin, düzgün kurulumu onaylamak için yerel bir
modelden çıktı alabilirler).

### **2. Hafta:** *Temel Teknikler -- Embeddings, Vektör Araması & SQLite*

**Konular & Faaliyetler:**

-   **Embeddings & Vektör Benzerliği (Vector Similarity):** Semantik anlamı
    yakalayan metinlerin sayısal vektör temsilleri olan **text embeddings**
    kavramını tanıtın. Benzer metinlerin benzer vektörler oluşturarak (similar
    text → similar vectors) *anlamsal aramayı (semantic search)* nasıl
    sağladığını açıklayın. Bu, RAG'ın getirme (retrieval) adımı için temeldir.
    embeddings'lerin nasıl elde edilebileceğini (OpenAI'ın ada'sı gibi özel
    modeller veya yerel modeller aracılığıyla) ve benzerliğin nasıl ölçüleceğini
    (örneğin **cosine similarity (kosinüs benzerliği)** aracılığıyla) tartışın.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

    -   *Kaynak:* **Microsoft Learn -- "Tutorial: Build a RAG application"**,
        *"Generate document embeddings"* (Belge embedding'leri oluşturma) ve
        *"Search for relevant documents"* (İlgili belgeleri arama) bölümleri
        (resmi). Bu, bir belge listesi için embedding'ler üretmek üzere
        Foundry Local'ın Python SDK'sının nasıl kullanılacağını ve vektörlerin
        kosinüs benzerliğini hesaplayarak benzerlik aramasının nasıl
        gerçekleştirileceğini gösterir.
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

    -   *Egzersiz:* **Embedding demosu:** Küçük bir örnek cümle listesi sağlayın
        ve öğrencilerin her cümle için embedding üretmek üzere Foundry Local
        SDK'sını kullanmasını sağlayın (qwen3-embedding-0.6b gibi küçük bir
        embedding modeli kullanarak). Ardından, verilen bir sorgu için (o da embed
        edilmiş şekilde), benzerlik puanlarını hesaplamak ve en iyi eşleşmeyi
        bulmak için basit bir döngü kodlamalarını isteyin. Bu, resmi eğitimdeki
        kodlara (hali hazırda bir find_relevant() fonksiyonu içerir) dayanabilir
        ve vektör aramasının nasıl çalıştığını somutlaştıracaktır.
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   **SQLite ile Embeddings Saklama & Sorgulama:** Bellek içi birkaç belgenin
    ötesine geçerken neden bir **vektör deposuna (vector store)** veya veritabanına
    ihtiyaç duyabileceğimizi açıklayın. Bizim kullanım senaryomuz için mükemmel
    olan *hızlı, sunucusuz yerel bir veritabanı motoru* olarak **SQLite**'ı
    tanıtın (ayrı bir sunucu veya kurulum gerektirmez; tek bir dosya tüm
    verileri tutar). Öğrencilerin temel **SQL** işlemlerini (tablolar oluşturma,
    veri ekleme ve sorgulama) en azından kavramsal olarak anladıklarından
    emin olun.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/apps/develop/data-access/sqlite-data-access)

    -   *Kaynak:* SQLite'ın avantajlarına ilişkin kilit noktalar için *"Benefits
        of SQLite for local storage"* (yerel depolama için SQLite'ın faydaları -
        *Microsoft Windows App Development* dokümantasyonundaki bir bölüm).
        İsteğe bağlı olarak, başlangıç dostu bir **SQLite öğreticisi** kullanın
        (örneğin, **W3Schools SQL tutorial**, "SQLite SELECT" sayfaları --
        üçüncü taraf olduğu net bir şekilde belirtilerek).
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/windows/apps/develop/data-access/sqlite-data-access)

    -   *Egzersiz:* **SQL oyun alanı (sandbox):** Öğrencilerin sqlite3 komut
        satırı aracını yüklemelerini veya küçük bir veritabanı (örneğin id,
        content, embedding alanları olan bir documents tablosu) oluşturmak için
        yerleşik sqlite3 modülünü içeren basit bir Python betiği kullanmalarını
        sağlayın. Birkaç örnek satır **ekleme (inserting)** ve bir id'ye göre
        kayıt çekmek veya metin anahtar kelimesine göre filtrelemek için bir
        **sorgu (query)** çalıştırma alıştırması yapmalarını sağlayın. Bu, verileri
        kalıcı hale getirme ve geri getirme sürecine aşinalık kazandırır --
        SQLite'ı RAG boru hattına entegre ettiklerinde ihtiyaç duyacakları
        becerilerdir.

-   **Soru-Cevap için Temel Prompt Engineering:** Yalnızca belgeleri getirmenin
    neden yeterli olmadığını tartışın -- *bilgiyi modele nasıl sunduğumuz
    önemlidir*. **System vs user prompts (Sistem ve kullanıcı istemleri)**
    kavramını (Chat Completion API'sindeki roller) ve modele getirilen metni
    kullanmasını, bunun ötesinde tahminde bulunmamasını nasıl talimatlandıracağınızı
    tanıtın. *"Bağlamda bilgi bulamazsan, bilmediğini söyle"* veya *"yanıtta
    her zaman kaynak adlarını ekle"* gibi basit kılavuz ilkeleri paylaşın.

    -   *Kaynak:* İstem oluşturmanın *temelleri (Basics)* ve *sistem mesajlarının
        (system messages)* kullanımı üzerine **Microsoft Learn -- "Prompt
        engineering techniques"** (resmi).
        [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering)

    -   *Egzersiz:* **İstem deneyleri:** Halka açık bir web yapay zekası (büyük
        olasılıkla karşılaştıkları Bing Chat veya ChatGPT gibi) kullanarak,
        öğrencilerin *aynı soruyu ek bağlamla ve ek bağlam olmadan* vermeyi
        denemelerini sağlayın (örneğin, "Yalnızca şu bilgiyi kullanarak yanıtla:
        \[bir pasaj sağlayın\]"). Bağlamın yanıtı nasıl değiştirdiğini gözlemleyin.
        Bu, kendi RAG sohbet robotlarının yapacağı işe kavramsal bir paralelliktir.

**2. Hafta sonundaki Kilometre Taşları (Milestones):** Öğrenciler **RAG, Foundry Local,
embeddings ve SQLite** hakkında çalışma bilgisine sahiptir. Test amaçlı bir SQLite
veritabanı oluşturmuşlardır (veya en azından belgeleri ve vektörleri saklamak
için şemayı kavramsal olarak tasarlamışlardır). Ayrıca Python'da embeddings'ler
üzerinde kosinüs benzerliği hesaplayarak benzer metinleri geri getirme alıştırmaları
yapmışlardır ve model için temel istemleri nasıl ifade edeceklerini anlamışlardır.
**Pratik kurulum için tüm önkoşullar hazırdır.**
[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
[\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

## **Phase 2 (3-4. Haftalar): Proje Uygulaması**

**Hedefler:** Yaklaşık 2 hafta boyunca öğrenciler **işlevsel bir yerel RAG uygulaması
geliştireceklerdir**. Her bir bileşeni uygulamak için öğrendiklerini uygulayacaklar:
belge alımı (ingestion), vektörleştirme (vectorization), getirme (retrieval)
ve LLM entegrasyonu. Aşaması 2'nin sonunda, her öğrenci (veya ekip), modeli
çağırmadan önce yerel belge deposundan bilgi alarak soruları yanıtlayabilen
**çalışan bir çevrimdışı soru-cevap sohbet robotuna (chatbot)** sahip olacaktır.

### **3. Hafta:** *Veri Alımı (Data Ingestion) & Getirme Boru Hattı (Retrieval Pipeline)*

**Konular & Faaliyetler:**

-   **Bilgi Tabanını Tasarlama & Veri Hazırlama:** Soru-cevap asistanı için
    küçük bir belge seti belirleyin (örneğin eğitmen tarafından sağlanan veya
    öğrenciler tarafından seçilen teknik makaleler, ürün SSS'leri veya ders
    notları gibi 5-10 kısa belge). Belgeleri parçalara (chunks) ayırma
    stratejilerini tartışın (RAG genellikle pasaj düzeyinde parçalarla çalıştığı
    için, örneğin her biri yaklaşık 1-3 paragraf). Öğrenciler şunları yapmak için
    bir **veri alımı betiği (data ingestion script)** uygulayacaklar:
    [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

1.  Belgelerini daha küçük pasajlara **bölmek (chunk)**.

2.  Foundry Local'ın embedding modelini kullanarak her bir parça (chunk) için
    bir **embedding** hesaplamak.

3.  Daha sonra geri getirmek üzere her bir parçayı ve embedding vektörünü
    SQLite'ta **saklamak (store)**.

-   *Kaynak:* **Microsoft Learn -- "Build a RAG application"** (resmi). *Creating
    a knowledge base* (bilgi tabanı oluşturma) ve *generating embeddings*
    (embeddings üretme) bölümlerini takip edin. Öğreticinin örnek kodu (Python)
    uyarlanabilir: belgeleri okumayı, toplu olarak embedding'ler üretmeyi ve
    bunları bir Python listesine kaydetmeyi gösterir (biz bunu SQLite'a kaydetmeye
    genişleteceğiz).
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   *Egzersiz:* **Veri Alımı Boru Hattını (Ingestion Pipeline) Kodlama:** Kendi
    main.py dosyalarında (veya ayrı bir betik/modülde), her öğrenci her belgeyi
    açmak, onu bölmek (örneğin paragraflara veya başlıklara göre) ve her bir
    parçayı embed etmek için Foundry Local SDK'sını kullanmak üzere kod yazar.
    Her bir parçayı (metin ve embedding vektörü) veritabanına eklemek (insert)
    için Python sqlite3 kütüphanesini kullanın. Basitleştirmek için, embedding
    bir blob veya metin (JSON ile serileştirilmiş vektör) olarak saklanabilir.
    **Test**: Veri alımını çalıştırdıktan sonra, veritabanının beklenen sayıda
    girdiye sahip olduğunu doğrulayın. İsteğe bağlı olarak, belgeler eklendiğinde
    veya değiştirildiğinde veri alımını yeniden çalıştırmak için basit bir
    **kurulum betiği (setup script)** oluşturun.

-   **Getirme Fonksiyonunun (Retrieval Function) Oluşturulması:** Veriler hazır
    olduğunda, yeni bir kullanıcı sorgusu verildiğinde ilgili parçaları getirme
    mantığını uygulayın. Öğrenciler şunları yapacaktır:

1.  **Sorguyu embed etmek** (aynı embedding modelini kullanarak).

2.  SQLite'ta **benzer vektörleri aramak** -- buradaki en basit yaklaşım, saklanan
    tüm embedding'leri çekmek (veya varsa bir SQL uzantısı kullanmak) ve
    Python'da kosinüs benzerliğini hesaplayıp ardından en iyi K parçayı (top-K
    chunks) seçmektir. *(Küçük N için bu yeterlidir; büyük N için özel vektör
    veritabanlarının veya SQL uzantılarının kullanılmasının gerekeceğini tartışın)*.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

3.  En üstteki parçaları bağlam (context) olarak **döndürmek**.

-   *Kaynak:* *find_relevant()* için **Microsoft'un öğretici kodu** (bizim
    ölçeğimiz için uygun olan, her belge için benzerliği kaba kuvvet - brute-force
    yöntemiyle arar). Ayrıca **RAG boru hattı** kararlarına (kaç parçanın
    getirileceği vb.) ilişkin Tech Community blog bölümüne bakın.
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app),
    [\[learn.microsoft.com\]](https://learn.microsoft.com/en-us/azure/foundry-local/tutorials/tutorial-build-rag-app)

-   *Egzersiz:* **Sorgu Getirmeyi Uygulama & Test Etme:** Kodda, kullanıcı sorgusu
    verildiğinde SQLite veritabanından en alakalı 2-3 parçayı döndüren bir
    get_top_chunks(query) fonksiyonu uygulayın. Bu fonksiyonu, mevcut verilere
    karşı birkaç örnek sorguyla test edin. Örneğin, belgelerden birinin kapsadığını
    bildiğiniz sorular sorun ve getirilen metin parçalarının alakalı göründüğünü
    doğrulayın. SQLite kullanılıyorsa, bu, sorgu vektörüyle karşılaştırmak için
    tüm vektörlerin belleğe okunmasını içerebilir (küçük veri kümemiz için kabul
    edilebilirdir). Kendinize güveniyorsanız ek bir zorluk: özel bir mesafe
    fonksiyonuna sahip bir **SQL sorgusu** kullanın veya harici bir vektör
    veritabanı kullanılıyorsa *vektör benzerliği (vector similarity)*
    özelliklerine dayanın -- ancak bu isteğe bağlıdir.

**3. Hafta sonundaki Kilometre Taşları (Milestones):** Öğrenciler **embeddings içeren
ve doldurulmuş bir SQLite belge veritabanına** ve verilen bir sorgu için en alakalı
belge parçalarını bulabilen çalışan bir **getirme fonksiyonuna (retrieval
function)** sahiptir.

### **4. Hafta:** *LLM Entegrasyonu & Uygulama Birleştirme (Assembly)*

**Konular & Faaliyetler:**

-   **Yerel LLM Entegrasyonu (Foundry Local Chat Modeli):** Şimdi bu getirme
    mekanizmasını yanıtlar üretmek üzere bir dil modeline bağlayın. Öğrenciler
    Foundry Local aracılığıyla uygun bir **küçük LLM** (örneğin *Phi-3.5 Mini
    veya benzeri 3-5 milyar parametreli bir model*) yükleyecek ve bunu
    **sohbet tarzında (chat-style)** yanıtlar üretmek için kullanacaklardır.
    Model seçimi ödünleşimlerini (trade-offs) tartışın: daha küçük modeller daha
    hızlı yanıt verir, ancak daha büyük modeller daha iyi yanıtlar sağlar -- bu
    programda öğrencilerin hızlı geri bildirim alabilmesi için hıza öncelik
    veriyoruz.

    -   *Kaynak:* *Yerel chat completions API*'sinin (çok turlu sohbet için)
        kullanılmasına ilişkin **Foundry Local Quickstart** bölümü. Bununla
        birlikte, daha basit bir yol: bunu tek turlu soru-cevap olarak ele
        almaktır. Öğrencilerin modelden nasıl bir **chat istemcisi (chat
        client)** oluşturacaklarını ve dokümantasyonda gösterildiği gibi
        completeChat veya benzerini nasıl çağıracaklarını gördüklerinden emin
        olun.
        [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/),
        [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

    -   *Egzersiz:* **Modeli Isındırma (Warm-up):** Öğrenciler, seçtikleri
        Foundry Local modelini program başlangıcında yüklemek için kod yazarlar
        (veri alımı sırasında zaten yüklenmemişse). Daha sonra, bağlamı getirmek
        için 3. Haftadaki getirme fonksiyonunu get_top_chunks() kullanan ve
        ardından yerel modelin chat API'sini, modele bağlamı kullanarak yanıt
        vermesini (ve dış bilgiyi kullanmamasını) talimatlandıran bir **sistem
        mesajı (system message)** ve ardından **kullanıcının sorusu** ile çağıran
        bir answer_query(user_question) fonksiyonu yazarlar. Basit bir soruyla
        **boru hattını uçtan uca test edin** ve yanıtı inceleyin.
        [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

-   **Basit Bir Kullanıcı Arayüzü (User Interface) Oluşturma:** Zamana ve
    öğrenci becerilerine bağlı olarak, soru-cevap asistanının arayüzünün nasıl
    çalışacağına dair seçenekler sunun:

    -   **Seçenek A: CLI (Komut Satırı Arayüzü)** -- en basit yol. Öğrenciler
        konsol üzerinden bir girdi sorgusu isteyebilir, answer_query(query)
        çağırabilir ve yanıtı yazdırabilir. Bu, odağın arka uç (backend)
        mantığında kalmasını sağlar.

    -   **Seçenek B: Streamlit veya Gradio Arayüzü** (Python) -- görselleştirme
        için harikadır. Kullanıcı bir soru gönderdiğinde answer_query
        fonksiyonunu çağıran minimal bir Streamlit uygulaması sağlayın. Bu,
        basit bir web arayüzü sunar (ve platformlar arasıdır).

    -   **Seçenek C: Temel HTML+JS Arayüzü** -- (öğrenciler web geliştirme
        deneyimi istiyorlarsa). Blogun yaklaşımını yeniden kullanabilirler:
        yanıtlar için yerel bir Flask veya Node sunucu uç noktasını (endpoint)
        çağıran bazı JavaScript kodları ve metin kutusu içeren statik bir HTML
        sayfası. Seçenek A'nın tercih edilmesi, zaman çerçevesi içinde
        tamamlanmayı garanti eder; Seçenek B/C ise ileri düzey öğrencilere veya
        zaman kalırsa 5. Hafta için ek hedefler (stretch goals) olarak
        sunulabilir.

    -   *Kaynak:* **Streamlit dokümantasyonu** (üçüncü taraf) veya *temel bir
        Flask/Express öğreticisi* (Seçenek C ise). İsteğe bağlı olarak, Tech
        Community blogunun örneğinin Express.js arka ucu tarafından sunulan
        tarayıcı tabanlı bir kullanıcı arayüzü olduğunu gösterin.
        [\[azurefeeds.com\]](https://azurefeeds.com/2026/03/30/building-your-first-local-rag-application-with-foundry-local/)

    -   *Egzersiz:* **Uygulama Arayüzünü Tamamlama:** Seçilen arayüzü uygulayın.
        CLI için, kullanıcının birden fazla soru sormasına izin vermek için
        input() fonksiyonunu döngüye alın. Web arayüzü için, minimal arayüz
        öğelerini kurmak ve arka uçla entegre etmek için kılavuzu takip edin.
        *Kapsamlı bir şekilde test edin:* uçtan uca işlevselliği doğrulamak için
        arayüz üzerinden çeşitli sorular sorun -- getirme işleminin
        gerçekleştiğinden emin olun (doğrulama için getirilen parçaları loglayabilirsiniz)
        ve modelin tutarlı bir şekilde yanıt verdiğini doğrulayın.

-   **Sorumlu Çıktılar Sağlama:** Öğrencilere prompt engineering en iyi
    uygulamalarını uygulamalarını hatırlatın: örneğin, bağlam yetersizse
    asistanın bilmediğini söylemesi talimatını her zaman ekleyin **(yanıt
    uydurmaktan - fabrikasyondan kaçınmak için)**. Kibar ve özlü yanıtlar için
    sistem istemlerine ince ayar yapmaya teşvik edin. Zaman elverirse,
    *kaynak atıfları (source citations)* eklemelerini sağlayın: örneğin, her
    parçayla birlikte kısa bir kaynak adı saklayarak modelin referansla yanıt
    vermesini sağlayın ("Belge X'e göre ..."). Bu, istemdeki talimatlar eklenerek
    veya gerekirse basit bir son işlem (post-processing) ile yapılabilir.

**4. Hafta sonundaki Kilometre Taşları (Milestones):** Her ekibin, kullanıcının
sorusunu (seçtikleri arayüz üzerinden) alabilen ve *SQLite destekli bilgi
tabanlarından* getirilen içeriği kullanarak yerel LLM tarafından oluşturulan bir
yanıtı döndürebilen **çalışan bir soru-cevap uygulaması** vardır. Temel proje
işlevselliği tamamlanmıştır.

## **Phase 3 (5-6. Haftalar): Test, Değerlendirme & Dokümantasyon**

**Hedefler:** Son aşamada, öğrenciler uygulamalarını geliştirecek ve test
edecek, performansı ile doğruluğunu değerlendirecek ve dokümantasyon ile bir
sunum hazırlayacaklardır. Bu aşamanın sonunda projeler cilalanmış ve gösterime
hazır hale getirilmiş olmalıdır.

### **5. Hafta:** *Sistem Testi & Değerlendirme*

**Konular & Faaliyetler:**

-   **Fonksiyonel Test (Functional Testing):** Öğrenciler, asistanlarının
    çeşitli sorgular için çalıştığından emin olmak için test senaryoları (test
    cases) geliştirirler (hem yanıtlayabileceği sorgular hem de yanıtlayamaması
    gerekenler için). Şunları doğrulamalıdırlar:

    -   Sistem, yanıt belgelerde mevcut olduğunda **ilgili bilgileri içeren bir
        yanıt döndürür**.

    -   Bilgi eksik olduğunda **uygun şekilde yanıt verir** (örneğin, sistem
        istemi talimatına göre "Bu bilgiye sahip değilim" gibi bir yedek -
        fallback mesajı döndürür).

    -   Uç durumları (edge cases) ele alır (boş sorgu girdisi veya çok genel
        sorular gibi). \*Yaklaşım:\* Öğrenciler, botlarını sistematik olarak test
        etmek için küçük bir soru-cevap seti (bazıları belgelerden
        yanıtlanabilir, bazıları yanıtlanamaz) derleyebilirler. Mümkünse,
        "gerçek kullanıcıları" simüle etmek için ekipler arasında test
        sorularını takas edin. Her test sorgusu için programlarını çalıştırmalı
        ve çıktıları kaydetmelidirler.

-   **Performans & Hata Ayıklama (Debugging):** Her şey yerel olduğundan, yanıt
    sürelerinin makul olduğunu kontrol edin (küçük modeller için, örneğin tipik
    bir dizüstü bilgisayarda soru başına yaklaşık 1-3 saniye). Yanıtlar
    yavaşsa, potansiyel optimizasyonları tartışın (örneğin daha az parça
    getirmek, daha küçük bir model kullanmak veya bunları önbelleğe alarak
    embeddings'leri tekrar tekrar hesaplamamaktan emin olmak). Öğrencilerin
    yanlış getirme sonuçları veya yanıtlardaki biçimlendirme sorunları gibi
    bekleyen sorunları ayıklamasına (debug) yardımcı olun.

-   **Değerlendirme ve İyileştirme:** Öz eleştiriyi ve yinelemeyi (iteration)
    teşvik edin. Öğrencilere şu soruları düşündürün: *Yanıtlar doğru mu? İyi
    yazılmış ve özlü mü? Kaynaklar belirtilmiş mi (eğer bu bir hedef idiyse)?*
    Değilse, yaklaşımlarını nasıl geliştirebilirler (örneğin, istem biçimini
    ayarlamak, daha fazla bağlam getirmek veya parça bölmeyi iyileştirmek)?
    Bu, kritik düşünme becerilerini uygulama ve proje kalitelerini artırma
    fırsatıdır.

**5. Haftanın Ortasındaki Kilometre Taşı (Milestone):** **Test sonuçları**
dokümante edilmiştir -- denenen sorguların listesi ve yanıtların doğru/uygun olup
olmadığı. Öğrenciler tüm eksiklikleri belirlemeli ve nihai ayarlamaları
planlamalıdır.

### **6. Hafta (veya 5. Haftanın sonu):** *Dokümantasyon & Nihai Sunum*

*(Mevcut zamana bağlı olarak, dokümantasyon ve sunum hazırlığı 5. Haftanın
sonlarında test etme ile çakışabilir veya 6. Haftaya uzayabilir.)*

**Konular & Faaliyetler:**

-   **Proje Dokümantasyonu:** Her ekip, projenin amacını, nasıl çalıştığını,
    uygulamayı çalıştırma talimatlarını ve tüm tasarım kararlarını veya
    sınırlamalarını detaylandıran kısa bir **Proje Raporu / README** yazar.
    Ortamın nasıl kurulacağını ve asistanın nasıl kullanılacağını
    eklediklerinden emin olun (bu aynı zamanda onların anlayışını da pekiştirir).
    Microsoft Learn modülleri veya öğreticileri takip edildiyse, öğrenciler
    bunlara atıfta bulunmalıdır.

-   **Kod Temizliği & Yorum Satırları:** Öğrenciler netlik için kodlarını gözden
    geçirirler. Hata ayıklama çıktılarını (debug prints) kaldırmalı, anahtar
    bölümleri açıklayan yorum satırları eklemeli (örneğin getirme fonksiyonunun
    ne yaptığını) ve kod stillerinin tutarlı olmasını sağlamalıdırlar. Bu nokta,
    daha önceden bilinmediği sürece kapsamlı bir Git/GitHub girişinin kapsam
    dışında kalmasına rağmen, en iyi uygulamaları vurgulamak için sürüm
    kontrolünden (version control) kısaca bahsetmek için iyi bir zamandır.

-   **Nihai Sunum Hazırlığı:** Her grup programın sonunda yerel RAG asistanlarının
    **kısa bir demosu ve sunumunu** gerçekleştirecektir. Onları şunları
    vurgulamaya yönlendirin:

    -   **Problem Tanımı (Problem Statement):** Asistanları hangi senaryoyu veya
        kullanıcı ihtiyacını hedefliyor?

    -   **Temel Özellikler/Bileşenler:** RAG'ı nasıl kullandığını, hangi veri
        kaynaklarını dahil ettiklerini vb. kısaca açıklayın.

    -   **Canlı Demo (Live Demo):** Belirsiz sorguları sorumlu bir şekilde ele
        aldığını kanıtlamak için, asistanın bir kaynak belirttiği veya bilmediğini
        söylediği bir soru da dahil olmak üzere birkaç örnek soruyu yanıtladığını
        gösterin.

    -   **Kazanılan Deneyimler (Lessons Learned):** Karşılaştıkları veya
        üstesinden geldikleri bir veya iki fikir ya da zorluk (örneğin,
        "belgeleri düzgün şekilde bölmenin iyi getirme sonuçları için çok
        önemli olduğunu öğrendik"). İsteğe bağlı olarak, sunum güvenini ve
        katılımını artırmak için asistanlarını adlandırmak veya arayüzü
        özelleştirmek gibi yaratıcı unsurları teşvik edin.

**6. Hafta sonundaki Kilometre Taşları (Milestones):** Tüm ekipler **dokümantasyonu
olan tamamlanmış projelere** (nihai bir rapor veya README) sahiptir ve
**sunumlarını/demolarını** prova etmişlerdir. Program, her ekibin çalışan yerel
RAG asistanlarını sunduğu ve öğrendikleri üzerinde düşündüğü bir **demo günü**
ile sona erer.

Program boyunca vurgu, küratörlü kaynaklarla desteklenen **pratik öğrenme (hands-on learning)** üzerindedir. Microsoft'un resmi rehberliğini (kurulum talimatları, eğitimler) pratik kodlama egzersizleriyle birleştirerek öğrenciler, nihai projeye entegre etmeden önce her bir bileşende kademeli olarak güven ve yetkinlik kazanırlar. **Ayın sonunda, işlevsel, çevrimdışı bir yapay zeka soru-cevap sistemine** -- ve yerel olarak çalıştırarak **getirme (arama) ve üretim (LLM)** yeteneklerini birleştirerek modern yapay zeka uygulamalarının nasıl oluşturulabileceğine dair sağlam bir anlayışa sahip olacaklardır.

Bu plan, temel konuların -- Foundry Local, RAG, embeddings, vektör araması (vector search), veri yönetimi ve prompt engineering -- erken tanıtılmasını ve ardından adım adım uygulanmasını sağlayarak başlangıç seviyesindeki öğrencilere ilk yerel RAG uygulamalarını başarıyla uygulama ve sergileme bilgi ve deneyimini kazandırır.
