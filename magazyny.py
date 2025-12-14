import streamlit as st

# Lista przechowująca produkty w magazynie
magazyn = []

# Funkcja do dodania produktu do magazynu
def dodaj_produkt(nazwa, ilosc):
    magazyn.append({'nazwa': nazwa, 'ilosc': ilosc})

# Funkcja do usunięcia produktu z magazynu
def usun_produkt(nazwa):
    global magazyn
    magazyn = [produkt for produkt in magazyn if produkt['nazwa'] != nazwa]

# Strona aplikacji Streamlit
st.title("Prosty Magazyn")

# Dodanie nowego produktu
st.header("Dodaj Nowy Produkt")
nazwa_produktu = st.text_input("Nazwa Produktu")
ilosc_produktu = st.number_input("Ilość Produktu", min_value=1, value=1)

if st.button("Dodaj Produkt"):
    if nazwa_produktu and ilosc_produktu > 0:
        dodaj_produkt(nazwa_produktu, ilosc_produktu)
        st.success(f"Produkt '{nazwa_produktu}' został dodany do magazynu.")
    else:
        st.error("Wszystkie pola muszą być wypełnione poprawnie.")

# Usuwanie produktu
st.header("Usuń Produkt")
usun_nazwa = st.text_input("Nazwa Produktu do Usunięcia")

if st.button("Usuń Produkt"):
    if usun_nazwa:
        usun_produkt(usun_nazwa)
        st.success(f"Produkt '{usun_nazwa}' został usunięty z magazynu.")
    else:
        st.error("Podaj nazwę produktu do usunięcia.")

# Wyświetlenie aktualnego stanu magazynu
st.header("Stan Magazynu")
if magazyn:
    for produkt in magazyn:
        st.write(f"{produkt['nazwa']} - Ilość: {produkt['ilosc']}")
else:
    st.write("Magazyn jest pusty.")
