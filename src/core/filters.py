from abc import ABC, abstractmethod
from distutils.command.install import value


class BaseFilter(ABC):
    def __init__(self, field_name=None, look_expression=None, label=None):
        self.field_name = field_name
        self.look_expression = look_expression or "eq"
        self.label = label

    @abstractmethod
    def filter(self, query, value, model):
        pass

    def get_lookup_expression(self, model):
        parts = self.field_name.split("__")
        column = getattr(model, parts[0])
        for part in parts[1:]:
            related_model = column.property.mapper.class_
            column = getattr(related_model, part)
        return column


class StringFilter(BaseFilter):
    def filter(self, query, value, model):
        if not value:
            return query

        column = self.get_lookup_expression(model=model)

        if self.look_expression == "eq":
            condition = column == value
        elif self.look_expression == "icontains":
            condition = column.ilike(f"%{value}%")
        elif self.look_expression == "startswith":
            condition = column.ilike(f"{value}%")
        else:
            raise ValueError(f" Lookup expression {self.look_expression} not supported")

        return query.filter(condition)


class NumberFilter(BaseFilter):
    def filter(self, query, value, model):
        if not value:
            return query

        try:
            value = float(value)
        except (TypeError, ValueError):
            return query

        column = self.get_lookup_expression(model=model)

        lookups = {
            "eq": column == value,
            "gt": column > value,
            "gte": column >= value,
            "lt": column < value,
            "lte": column <= value,
        }

        condition = lookups.get(self.look_expression)
        if condition is None:
            raise ValueError(f"Lookup expression {self.look_expression} not supported")

        return query.filter(condition)


class BooleanFilter(BaseFilter):
    def filter(self, query, value, model):
        if value is None or value == "":
            return query

        if isinstance(value, str):
            value = value.lower() in ("true", "1", "yes")
        else:
            value = bool(value)

        column = self.get_lookup_expression(model=model)
        return query.filter(column == value)


class FilterSet:
    def __init__(self, data, query, model):
        self.data = data or {}
        self.query = query
        self.model = model
        self.filters = self._get_filters()

    def _get_filters(self):
        filters = {}
        for name, attr in self.__class__.__dict__.items():
            if isinstance(attr, BaseFilter):
                if attr.field_name is None:
                    attr.field_name = name
                filters[name] = attr
        return filters

    def filter_query(self):
        qs = self.query

        for name, filter_instance in self.filters.items():
            value = self.data.get(name)
            if value == "":
                value = None

            if value is not None:
                qs = filter_instance.filter(qs, value, self.model)

        return qs

    @property
    def qs(self):
        return self.filter_query()


class UserFilterSet(FilterSet):
    first_name = StringFilter(look_expression="icontains")
    last_name = StringFilter(look_expression="startswith")
    email = StringFilter(look_expression="eq")
