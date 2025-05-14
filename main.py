from src.question import question
def main():
    for i in range(1,4):
        dogru_cevap = question(i)
        try:
            kullanici_cevabi = int(input())

            if kullanici_cevabi == dogru_cevap:
                print("✅ Doğru cevap!")
            else:
                print(f"❌ Yanlış cevap. Doğru cevap: {dogru_cevap}")
        except ValueError:
            print("⚠️ Lütfen sadece sayı girin!")

if __name__ == "__main__":
    main()