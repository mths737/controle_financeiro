def ordenar_queryset(queryset, btn_order, current_order, order_fields_map):
    """
    Aplica ordenação genérica.
    """
    new_order = "dec" if (btn_order == current_order and current_order == "cre") else "cre"
    field = order_fields_map.get(btn_order, list(order_fields_map.keys())[0])
    return queryset.order_by(field if new_order == "cre" else f"-{field}"), new_order