from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


def complete(self, design_image):
    """Завершить заявку: можно из 'new' или 'in_progress'"""
    if self.status not in ('new', 'in_progress'):
        return False
    if not design_image:
        return False
    self.status = 'completed'
    self.design_image = design_image
    self.save(update_fields=['status', 'design_image', 'updated_at'])
    return True


def validate_image_file(value):
    """Валидатор изображения: формат и размер ≤ 2 МБ"""
    allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            _('Разрешены только файлы форматов: JPG, JPEG, PNG, BMP.')
        )
    if value.size > 2 * 1024 * 1024:  # 2 МБ
        raise ValidationError(_('Размер файла не должен превышать 2 МБ.'))


class CustomUser(AbstractUser):
    # ФИО: только кириллица, пробел, дефис
    full_name = models.CharField(
        max_length=150,
        verbose_name=_('ФИО'),
        validators=[
            RegexValidator(
                regex=r'^[а-яА-ЯёЁ \-]+$',
                message=_('ФИО может содержать только кириллические буквы, пробел и дефис.')
            )
        ]
    )

    class Meta:
        ordering = ['full_name']
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user-detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название категории'),
        help_text=_("Например: 3D-дизайн, Эскиз и т.д.")
    )


    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    STATUS_CHOICES = (
        ('new', _('Новая')),
        ('in_progress', _('Принято в работу')),
        ('completed', _('Выполнено')),
    )

    title = models.CharField(max_length=200, verbose_name=_('Название'))
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Описание'),
        help_text=_('Опишите помещение и пожелания по дизайну')
    )
    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Клиент'),
        related_name='design_requests'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('Категория')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_('Статус')
    )
    plan_image = models.ImageField(
        upload_to='plans/%Y/%m/%d/',
        verbose_name=_('План помещения'),
        validators=[validate_image_file]
    )
    design_image = models.ImageField(
        upload_to='designs/%Y/%m/%d/',
        verbose_name=_('Готовый дизайн'),
        blank=True,
        null=True,
        validators=[validate_image_file]
    )
    admin_comment = models.TextField(
        verbose_name=_('Комментарий администратора'),
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('Уникальный ID заявки')
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        permissions = (
            ("can_change_status", _("Может изменять статус заявки")),
            ("can_view_all", _("Может просматривать все заявки")),
        )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def can_be_deleted(self):
        """Можно удалить, только если статус — 'Новая'"""
        return self.status == 'new'

    def take_to_work(self, comment):
        """Принять заявку в работу"""
        if self.status != 'new':
            return False
        self.status = 'in_progress'
        self.admin_comment = comment
        self.save(update_fields=['status', 'admin_comment', 'updated_at'])
        return True

    def complete(self, design_image):
        """Завершить заявку: можно из 'new' или 'in_progress'"""
        if self.status not in ('new', 'in_progress'):
            return False
        if not design_image:
            return False  # изображение обязательно при завершении
        self.status = 'completed'
        self.design_image = design_image
        self.save(update_fields=['status', 'design_image', 'updated_at'])
        return True

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('request-detail', args=[str(self.id)])