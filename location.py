def handle_permission(gl, AlertDialog, page, Text, TextButton,MainAxisAlignment):
    status = gl.get_permission_status()
    if str(status) == "GeolocatorPermissionStatus.WHILE_IN_USE" or str(status) == "GeolocatorPermissionStatus.ALWAYS":
        pass
    else:
        def handle_click(e):
            gl.open_app_settings()
        def handle_check(e):
            status = gl.get_permission_status()
            if str(status) == "GeolocatorPermissionStatus.WHILE_IN_USE" or str(status) == "GeolocatorPermissionStatus.ALWAYS":
                page.close(dlg_modal)
            else: 
                page.close(dlg_modal)
                dlg_modal.content = Text("Per fer servir l'app necessitem accedir a l'ubicació! \n\nVols obrir la configuració de l'app per garantir accès? \n\nSeguim sense accès!")
                page.open(dlg_modal)
                page.update()
                print("no tenim access")
        
        print("no tenim access")
        dlg_modal = AlertDialog(
            modal=True,
            adaptive = True,
            title=Text("Error localització!"),
            content=Text("Per fer servir l'app necessitem accedir a l'ubicació! \n\nVols obrir la configuració de l'app per garantir accès?"),
            actions=[
                TextButton("Comprovar-ho", on_click=handle_check),
                TextButton("Si",on_click=handle_click),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        page.open(dlg_modal)

