from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope, Tag

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        tags = []
        for form in self.forms:
            if 'is_main' in form.cleaned_data:
                if form.cleaned_data['is_main']:
                    count += 1
            if count == 0:
                raise ValidationError('Какая-то ошибка')
            else:
                pass
            # Проверка на дублирование тега в одной статье
            if form.cleaned_data:
                tag = form.cleaned_data.get('tag')
                if tag in tags:
                    raise ValidationError("Тег не может быть добавлен дважды.")
                tags.append(tag)
        return super().clean()

class RelationshipInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Tag)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
