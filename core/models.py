import uuid
from clickhouse_backend import models as ch_models
from django.db import models
from clickhouse_driver import Client
from django.conf import settings

class GameData(models.Model):
    id = ch_models.UUIDField(primary_key=True, default=uuid.uuid4())
    app_id = ch_models.Int32Field(unique=True) 
    name = ch_models.StringField()
    release_date = ch_models.DateField()
    required_age = ch_models.Int32Field(default=0)  
    price = ch_models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    dlc_count = ch_models.Int32Field(default=0)  
    about_the_game = ch_models.StringField(default='')  
    supported_languages = ch_models.StringField(default='')  
    windows = ch_models.UInt8Field(default=0)  
    mac = ch_models.UInt8Field(default=0)  
    linux = ch_models.UInt8Field(default=0)  
    positive_reviews = ch_models.Int32Field(default=0)  
    negative_reviews = ch_models.Int32Field(default=0)  
    score_rank = ch_models.Int32Field(default=0)  
    developer = ch_models.StringField(default='')  
    publisher = ch_models.StringField(default='')  
    categories = ch_models.StringField(default='')  
    genres = ch_models.StringField(default='')  
    tags = ch_models.StringField(default='')  

    class Meta:
        db_table = 'game_data'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "app_id": self.app_id,
            "name": self.name,
            "release_date": self.release_date.isoformat(),
            "required_age": self.required_age,
            "price": self.price,
            "dlc_count": self.dlc_count,
            "about_the_game": self.about_the_game,
            "supported_languages": self.supported_languages,
            "windows": self.windows,
            "mac": self.mac,
            "linux": self.linux,
            "positive_reviews": self.positive_reviews,
            "negative_reviews": self.negative_reviews,
            "score_rank": self.score_rank,
            "developer": self.developer,
            "publisher": self.publisher,
            "categories": self.categories,
            "genres": self.genres,
            "tags": self.tags,
        }

    @classmethod
    def create_clickhouse_table(cls):
        """Create ClickHouse table if it doesn't exist."""
        client = Client(host=settings.DATABASES['default']['HOST'],
                        user=settings.DATABASES['default']['USER'],
                        password=settings.DATABASES['default']['PASSWORD'],
                        database=settings.DATABASES['default']['NAME'])
        
        # Check if table exists and create if not
        client.execute(f"""
        CREATE TABLE IF NOT EXISTS {cls._meta.db_table} (
            id UUID,
            app_id Int32,
            name String,
            release_date Date,
            required_age Int32,
            price Decimal(10, 2),
            dlc_count Int32,
            about_the_game String,
            supported_languages String,
            windows UInt8,
            mac UInt8,
            linux UInt8,
            positive_reviews Int32,
            negative_reviews Int32,
            score_rank Int32,
            developer String,
            publisher String,
            categories String,
            genres String,
            tags String
        ) ENGINE = MergeTree()
        ORDER BY (app_id);
        """)
