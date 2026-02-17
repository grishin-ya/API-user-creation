from django.db.models import QuerySet
from .models import CustomUser, Trainee

def get_trainees_for_user(user: CustomUser) -> QuerySet[Trainee]:
    """
    Возвращает список стажёров в зависимости от роли пользователя.
    """
    base_queryset = Trainee.objects.select_related(
        "mentor"
    ).prefetch_related(
        "directions"
    )

    if user.role == "HR":
        return base_queryset

    if user.role == "HEAD":
        return base_queryset.filter(
            directions__in=user.directions.all()
        ).distinct()

    if user.role == "MENTOR":
        return base_queryset.filter(mentor=user)

    return Trainee.objects.none()
