import threading
import time
import os

# Sabit PIN Listesi (örnek) ve MAC adresleri
pin_list = [
    "11532620", "42256403", "29048830", "55349284", "12422326",
    "47023253", "33916286", "15866653", "31452502", "18405446",
    "73368571", "83092138", "59390954", "58568729", "74988587",
    "78705586", "46400444", "65579206", "38376467", "57900568",
    "28288480", "54163607", "19739700", "19739700", "40909288",
    "57836041", "15511546", "36880447", "44785567", "43366729",
    "15253125", "49781984", "58297445", "52805127", "52812286",
    "48715560", "14648304", "11969129", "97358978", "24093361",
    "46394378", "51183868", "39883520", "27260333", "91267559",
    "30924284", "6629069", "69458750", "28549789", "2691459",
    "63102756", "75928345", "89028416", "14527643", "27483761",
    "32801482", "19938274", "28390265", "49837290", "76384920",
    "49382761", "28473650", "57483921", "72647391", "19283764",
    "90827364", "28573910", "39482076", "28394765", "75683921",
    "58749120", "94720358", "26482739", "73592046", "28374615",
    "52816349", "32859410", "17462938", "69324751", "39482765",
    "75948216", "10593847", "29483975", "68392047", "49562830",
    "34765891", "76283940", "82574829", "98374615", "74692851",
    "26459387", "38904261", "93572804", "63749285", "37482056",
    "47583920", "63849502", "19384756", "73592061", "28567394",
    "90384761", "56483729", "28473951", "17492736", "82956401",
    "37820361", "94857362", "28365149", "93574602", "16384925",
    "47392065", "52873649", "18374650", "97263850", "74829365",
    "27463851", "35894620", "82749360", "10592837", "49582730",
    "63947128", "28376490", "45873216", "38492075", "49832067",
    "73892604", "58374691", "20485739", "93746205", "58373928",
    "27649285", "64827395", "19376485", "94762301", "48273610",
    "73942851", "27483951", "58473629", "73948526", "28473650",
    "94863721", "37928465", "19038472", "68374692", "94720364",
    "11532620", "42256403", "29048830", "55349284", "12422326",
    "47023253", "33916286", "15866653", "31452502", "18405446",
    "73368571", "83092138", "59390954", "58568729", "74988587",
    "78705586", "46400444", "65579206", "38376467", "57900568",
    "28288480", "54163607", "19739700", "19739700", "40909288",
    "57836041", "15511546", "36880447", "44785567", "43366729",
    "15253125", "49781984", "58297445", "52805127", "52812286",
    "48715560", "14648304", "11969129", "97358978", "24093361",
    "46394378", "51183868", "39883520", "27260333", "91267559",
    "30924284", "6629069", "69458750", "28549789", "2691459"
]

# Log dosyası yolu
log_file = "wps_bruteforce_log.txt"

def write_log(message):
    """Log dosyasına yazma fonksiyonu"""
    with open(log_file, "a") as file:
        file.write(f"{time.ctime()}: {message}\n")

def load_pin_list_from_file(filename="pins.txt"):
    """PIN listesini dosyadan yükleyin"""
    if not os.path.exists(filename):
        write_log("PIN listesi dosyası bulunamadı. Sabit liste kullanılacak.")
        return pin_list  # Eğer dosya yoksa, sabit listeyi kullan
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def brute_force_wps(bssid, channel, pin_list_chunk, attempt_count):
    """WPS PIN brute force fonksiyonu"""
    global log_file
    for pin in pin_list_chunk:
        attempt_count += 1
        print(f"Deneme {attempt_count}: {pin}")
        write_log(f"Deneme {attempt_count}: PIN {pin} denendi.")
        
        # Burada WPS PIN kırma işlemi simüle ediliyor (örnek)
        # Gerçek saldırı için ilgili modül kullanılabilir (örneğin, Reaver)
        
        # Bu örnekte başarılı PIN bulunduğunda sonlandırıyoruz
        if pin == "15368949":  # Örnek başarılı PIN
            print(f"[BAŞARILI] Wi-Fi'ye bağlandı! PIN: {pin}")
            write_log(f"[BAŞARILI] PIN: {pin} ile bağlantı başarılı.")
            break

        # Her 10 denemede bir ilerleme mesajı yazdırılıyor
        if attempt_count % 10 == 0:
            print(f"İlerlemeniz: {attempt_count} PIN denemesi tamamlandı.")

def start_bruteforce(bssid, channel):
    """Çoklu iş parçacığı ile brute force başlatma"""
    # PIN listelerini çoklu iş parçacığına ayırma
    num_threads = 4  # 4 iş parçacığı kullanacağız
    pin_list_chunks = [pin_list[i::num_threads] for i in range(num_threads)]

    # İş parçacıklarını başlatma
    threads = []
    attempt_count = 0
    for i in range(num_threads):
        thread = threading.Thread(target=brute_force_wps, args=(bssid, channel, pin_list_chunks[i], attempt_count))
        threads.append(thread)
        thread.start()

    # İş parçacıklarının bitmesini bekle
    for thread in threads:
        thread.join()

def main():
    """Ana program fonksiyonu"""
    # Başlangıç mesajı
    print("WPS Brute Force Tool Başlatılıyor...\n")

    # PIN listesini dosyadan al
    pin_list = load_pin_list_from_file()

    # Kullanıcıdan BSSID ve kanal bilgisi al
    bssid = input("BSSID (Wi-Fi MAC adresi) girin: ")
    channel = input("Kanal numarasını girin: ")

    # Brute force işlemini başlat
    start_bruteforce(bssid, channel)

    print("\nSaldırı tamamlandı. Sonuçlar log dosyasına kaydedildi.")
    print("Log dosyasına bakmak için 'wps_bruteforce_log.txt' dosyasını kontrol edin.")

if __name__ == "__main__":
    main()
