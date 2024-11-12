from icalendar import Calendar as ICalendar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..event.models import Event
from ..exceptions import HTTPException, ResourceNotFound
from .models import Calendar


async def import_ics(
    file_content: bytes, user_id: int, db: AsyncSession, calendar_id: int = None
):
    try:
        # Parsear el archivo .ics
        ical = ICalendar.from_ical(file_content)

        # Buscar el calendario si calendar_id está definido
        calendar = None
        if calendar_id:
            result = await db.execute(
                select(Calendar).where(
                    Calendar.id == calendar_id, Calendar.user_id == user_id
                )
            )
            calendar = result.scalar_one_or_none()
            if not calendar:
                raise ResourceNotFound("Calendar not found")

        # Si no hay un calendario existente, crear uno nuevo
        if not calendar:
            calendar_name = "Imported Calendar"  # Podrías extraer
            calendar = Calendar(name=calendar_name, user_id=user_id)
            db.add(calendar)
            await (
                db.flush()
            )  # Hacer flush para obtener el ID del calendario recién creado

        # Iterar sobre los componentes del archivo .ics para crear eventos
        for component in ical.walk():
            if component.name == "VEVENT":
                # Extraer datos del evento
                title = component.get("summary")
                start = component.get("dtstart").dt
                end = component.get("dtend").dt
                description = component.get("description")

                # Crear un nuevo evento vinculado al calendario
                new_event = Event(
                    title=title,
                    description=description,
                    start_datetime=start,
                    end_datetime=end,
                    user_id=user_id,
                    calendar_id=calendar.id,
                )
                db.add(new_event)

        # Confirmar todos los cambios en la base de datos
        await db.commit()
        return {
            "detail": "Calendar and events imported successfully",
            "calendar_id": calendar.id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
