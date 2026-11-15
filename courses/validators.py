import re

from django.core.exceptions import ValidationError

YOUTUBE_REGEX = re.compile(
    r"^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}"
)


def validate_video_link(value: str):
    """
    Разрешает только ссылки на YouTube.
    Остальные ссылки — ошибка.
    """
    if not value:
        return

    if not YOUTUBE_REGEX.match(value):
        raise ValidationError(
            "Разрешены только ссылки на видео YouTube (youtube.com или youtu.be)."
        )
