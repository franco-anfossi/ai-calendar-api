from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    """Modelo de Pydantic para manejar los parámetros de paginación"""

    page: Optional[int] = Query(
        1, ge=1, description="Número de página, debe ser 1 o más"
    )
    per_page: Optional[int] = Query(
        10, ge=1, le=100, description="Número de elementos por página, entre 1 y 100"
    )


class Pagination(BaseModel):
    """Modelo para estructurar la respuesta paginada"""

    items: List  # Los elementos paginados
    total: int  # Total de elementos en la colección
    page: int  # Página actual
    per_page: int  # Elementos por página
    total_pages: int  # Total de páginas


def paginate(items: List, pagination_params: PaginationParams) -> Pagination:
    """
    Función para realizar la paginación de una lista de elementos.

    - `items`: Lista completa de elementos a paginar.
    - `pagination_params`: Instancia del modelo `PaginationParams` con los parámetros.

    Retorna una instancia del modelo `Pagination` con los elementos paginados.
    """
    page = pagination_params.page or 1
    per_page = pagination_params.per_page or 10
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]

    return Pagination(
        items=paginated_items,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,  # Calcular el total de páginas
    )
