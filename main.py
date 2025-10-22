import flet as ft
from flet.core import page

import automobile
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD)

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca = ft.TextField(label = "Marca") #in questo caso non serve mettere value perché l'utente deve scrivere i dati, mentre se non dovesse scriverli si inserisce in value quello che contiene il campo
    input_modello = ft.TextField(label = "Modello")
    input_anno = ft.TextField(label= 'Anno')

    txtOut = ft.TextField(width= 100, disabled=True,
                          value = '4', border_color = 'green',
                          text_align = ft.TextAlign.CENTER)

    def handleAdd(e): #INCREMENTO
        currentVal = int(txtOut.value)
        txtOut.value = str(currentVal + 1)
        txtOut.update()

    def handleRemove(e): #DIMINUZIONE
        currentVal = int(txtOut.value)
        txtOut.value = str(currentVal - 1)
        txtOut.update()

    btnMinus = ft.IconButton(
        icon = ft.Icons.REMOVE,
        icon_color = 'green',
        icon_size = 24,
        on_click = handleRemove)

    btnAdd = ft.IconButton(
        icon=ft.Icons.ADD,
        icon_color='green',
        icon_size=24,
        on_click=handleAdd)

    row_posti = ft.Row([ btnMinus, txtOut, btnAdd],
                       alignment = ft.MainAxisAlignment.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def aggiungi_automobile(e):
        marca = input_marca.value.strip()
        modello = input_modello.value.strip()
        anno = input_anno.value.strip()
        posti = txtOut.value.strip()

        try:
            prova_anno = int(anno)
        except ValueError:
            alert.show_alert("Errore: Valore non numerico per il campo anno ")
            return

        try:
            prova_posti = int(posti)
        except ValueError:
            alert.show_alert("Errore: Valore non numerico per il campo posti ")
            return

        autonoleggio.aggiungi_automobile(marca, modello, anno, posti) #aggiungere l'auto all'Autonoleggio

        input_marca.value = '' #svuoto i campi
        input_modello.value = ''
        input_anno.value = ''
        txtOut.value = '4'

        aggiorna_lista_auto() #aggiorno la lista

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btnAggiungiAuto = ft.ElevatedButton('Aggiungi automobile',
                                        on_click=aggiungi_automobile)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuova automobile", size=20),
        ft.Row(spacing=40,
               controls = [input_marca, input_modello, input_anno, row_posti, btnAggiungiAuto],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
