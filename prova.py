import flet as ft

def main(page: ft.Page):
    text_with_shadow = ft.Container(
        content=ft.Text("Text amb ombra", size=14, color="white"),
        shadow=ft.BoxShadow(
            spread_radius=1,  # Redueix el valor de spread_radius per fer l'ombra més petita
            blur_radius=100,    # Redueix el valor de blur_radius per fer l'ombra més definida
            color=ft.colors.BLACK,
            offset=ft.Offset(1, 1)  # Redueix l'offset per fer l'ombra més propera al text
        ),
        padding=ft.padding.all(10)
    )

    page.add(text_with_shadow)

ft.app(target=main)
