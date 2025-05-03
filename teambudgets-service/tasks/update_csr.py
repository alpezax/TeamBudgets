def run():
    from datetime import datetime, timedelta
    from model.trabajador import Trabajador
    from model.categoriaTrabajador import CategoriaTrabajador

    def get_next_months(n):
        """Devuelve una lista con los próximos n meses en formato YYYY-MM"""
        base = datetime.today().replace(day=1)
        return [(base + timedelta(days=32 * i)).strftime("%Y-%m") for i in range(n)]

    trabajador_model = Trabajador()
    categoria_model = CategoriaTrabajador()

    trabajadores = trabajador_model.get_all()
    meses_a_procesar = get_next_months(5)

    for t in trabajadores:
        trabajador_id = t["_id"]
        categoria_id = t.get("categoria")

        if not categoria_id:
            print(f"[WARN] Trabajador {trabajador_id} no tiene categoría asignada.")
            continue

        categoria = categoria_model.get_by_id(categoria_id)
        if not categoria:
            print(f"[WARN] Categoría {categoria_id} no encontrada.")
            continue

        default_csr = categoria.get("defaultcsr", 100)

        # Obtener el CSR más reciente del trabajador usando el nuevo método
        ultimo_coste = trabajador_model.get_ultimo_coste_hora(trabajador_id)
        coste_hora_actual = ultimo_coste["coste_hora"] if ultimo_coste else None

        for mes in meses_a_procesar:
            ya_informado = trabajador_model.get_coste_hora_mensual(trabajador_id, mes)
            if ya_informado is not None:
                print(f"[SKIP] Trabajador {trabajador_id} ya tiene coste para {mes}.")
                continue

            coste_hora = coste_hora_actual if coste_hora_actual is not None else default_csr

            success = trabajador_model.set_coste_hora_mensual(trabajador_id, mes, coste_hora)

            if success:
                print(f"[OK] Coste-hora {coste_hora} informado para {trabajador_id} en {mes}.")
            else:
                print(f"[FAIL] No se pudo informar coste-hora para {trabajador_id} en {mes}.")
