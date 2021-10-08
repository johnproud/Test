from parler.managers import TranslatableManager
from softdelete.managers import SoftDeleteManager


class SoftDeleteTranslatableDotsManager(SoftDeleteManager, TranslatableManager):
    def get(self, *args, **kwargs):
        return self.get_raw_queryset().get(*args, **kwargs)
