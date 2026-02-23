from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
import uuid

class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_BUCKET
    
    def _save(self, name, content):
        # Generate unique filename
        ext = name.split('.')[-1]
        unique_name = f"{uuid.uuid4()}.{ext}"
        
        # Upload to Supabase
        self.client.storage.from_(self.bucket).upload(
            unique_name,
            content.read(),
            file_options={"content-type": content.content_type}
        )
        return unique_name
    
    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket}/{name}"
    
    def exists(self, name):
        try:
            self.client.storage.from_(self.bucket).list(name)
            return True
        except:
            return False
    
    def delete(self, name):
        self.client.storage.from_(self.bucket).remove([name])