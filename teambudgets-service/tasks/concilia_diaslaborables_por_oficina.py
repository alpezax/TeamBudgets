def run():
    from model.trabajador import Trabajador
    from model.oficina import Oficina

    trabajador_model = Trabajador()
    oficina_model = Oficina()

    trabajadores = trabajador_model.get_all()

    for t in trabajadores:
        trabajador_id = t["_id"]
        oficina_id = t.get("oficina")

        if not oficina_id:
            print(f"[WARN] Trabajador {trabajador_id} no tiene oficina asignada.")
            continue

        oficina = oficina_model.get_by_id(oficina_id)
        if not oficina:
            print(f"[WARN] Oficina {oficina_id} no encontrada.")
            continue

        dias_laborables_dict = oficina.get("dias-laborables", {})

        if not dias_laborables_dict:
            print(f"[WARN] La oficina {oficina_id} no tiene días laborables definidos.")
            continue

        for periodo, dias in dias_laborables_dict.items():
            nueva_dedicacion = {
                "vacaciones": 0,
                "laborables": dias
            }

            success = trabajador_model.set_dedicacion_mensual(trabajador_id, periodo, nueva_dedicacion)

            if success:
                print(f"[OK] Actualizado {trabajador_id} para periodo {periodo} con {dias} días.")
            else:
                print(f"[FAIL] No se pudo actualizar {trabajador_id} para {periodo}.")
