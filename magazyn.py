import streamlit as st
import random
import string

# --- Inicjalizacja Magazynu (Lista Towarów) ---
# Używamy prostej listy Pythona jako naszego "magazynu".
# Zmienna ta jest inicjalizowana przy każdym uruchomieniu/odświeżeniu aplikacji Streamlit.
# W rzeczywistej aplikacji produkcyjnej użyłbyś st.session_state, bazy danych lub pliku do trwałości.
MAGAZYN = [
    {'nazwa': 'Komputer biurowy', 'ilosc': 5, 'kod': 'KB-101'},
    {'nazwa': 'Pralka automatyczna', 'ilosc': 3, 'kod': 'PA-202'},
    {'nazwa': 'Drabina metalowa', 'ilosc': 12, 'kod': 'DM-303'},
    {'nazwa': 'Młotek ciesielski', 'ilosc': 50, 'kod': 'MC-404'},
]

# Funkcja do generowania unikalnego kodu dla nowego produktu (uproszczona)
def generuj_kod(dlugosc=4):
    litery = string.ascii_uppercase
    cyfry = string.digits
    return 'TOW-' + ''.join(random.choice(litery) for i in range(2)) + ''.join(random.choice(cyfry) for i in range(dlugosc))


# --- Funkcje Logiki Magazynu ---

def dodaj_towar(nazwa, ilosc, kod):
    """Dodaje nowy towar do magazynu."""
    # Prosta walidacja
    if not nazwa or ilosc <= 0:
        st.error("Wprowadzono niepoprawne dane.")
        return False
        
    # Sprawdzenie, czy towar już istnieje po nazwie (w uproszczeniu)
    for towar in MAGAZYN:
        if towar['nazwa'].lower() == nazwa.lower():
            st.warning(f"Towar '{nazwa}' już istnieje. Zamiast dodawać, zwiększamy ilość.")
            towar['ilosc'] += ilosc
            return True

    # Dodanie nowego towaru
    MAGAZYN.append({
        'nazwa': nazwa,
        'ilosc': ilosc,
        'kod': kod if kod else generuj_kod()
    })
    st.success(f"Pomyślnie dodano towar: **{nazwa}** (Ilość: {ilosc})")
    return True

def usun_towar_po_kodzie(kod_towaru):
    """Usuwa towar z magazynu na podstawie jego unikalnego kodu."""
    global MAGAZYN # Użycie globalnej listy MAGAZYN
    
    # Tworzymy nową listę, pomijając towar o podanym kodzie
    nowy_magazyn = [towar for towar in MAGAZYN if towar['kod'] != kod_towaru]
    
    if len(nowy_magazyn) < len(MAGAZYN):
        usuniete = len(MAGAZYN) - len(nowy_magazyn)
        MAGAZYN = nowy_magazyn # Zastąpienie starej listy nową
        st.success(f"Pomyślnie usunięto {usuniete} towar(ów) o kodzie: **{kod_towaru}**")
        return True
    else:
        st.error(f"Nie znaleziono towaru o kodzie: **{kod_towaru}**")
        return False


# --- Interfejs Użytkownika Streamlit ---

st.set_page_config(page_title="Prosty Magazyn (Streamlit + Lista)", layout="wide")

st.title("📦 Prosty System Magazynowy")
st.markdown("Aplikacja demonstruje podstawowe operacje dodawania i usuwania towarów, używając zwykłej listy Python jako magazynu danych.")

st.subheader("📊 Stan Magazynu")
# Wyświetlanie listy towarów
if MAGAZYN:
    st.table(MAGAZYN)
else:
    st.info("Magazyn jest pusty.")

st.markdown("---")

# --- Operacje: Dodawanie Towaru ---
with st.expander("➕ Dodaj Nowy Towar do Magazynu"):
    with st.form("form_dodawanie"):
        st.markdown("#### Wprowadź dane nowego towaru")
        input_nazwa = st.text_input("Nazwa Towaru", key="nazwa_dodaj")
        input_ilosc = st.number_input("Ilość", min_value=1, step=1, value=1, key="ilosc_dodaj")
        input_kod = st.text_input("Kod Towaru (opcjonalny)", key="kod_dodaj")
        
        submitted_dodaj = st.form_submit_button("Dodaj Towar")
        
        if submitted_dodaj:
            dodaj_towar(input_nazwa.strip(), input_ilosc, input_kod.strip().upper())


# --- Operacje: Usuwanie Towaru ---
with st.expander("➖ Usuń Towar z Magazynu"):
    if MAGAZYN:
        kody_do_wyboru = [towar['kod'] for towar in MAGAZYN]
        
        with st.form("form_usuwanie"):
            st.markdown("#### Wybierz towar do usunięcia (na podstawie kodu)")
            
            kod_do_usuniecia = st.selectbox(
                "Kod Towaru do usunięcia",
                options=kody_do_wyboru,
                key="kod_usun"
            )
            
            submitted_usun = st.form_submit_button("Usuń Towar")
            
            if submitted_usun:
                usun_towar_po_kodzie(kod_do_usuniecia)
    else:
        st.warning("Brak towarów do usunięcia.")
