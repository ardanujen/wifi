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
