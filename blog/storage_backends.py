from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
import uuid
import os
import logging
logger = logging.getLogger(__name__)

class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_BUCKET
    
    def _save(self, name, content):
        logger.warning(f"[Supabase] _save called with name={name}")
        # Keep the folder structure (e.g., covers/ or avatars/)
        folder = os.path.dirname(name)
        ext = os.path.splitext(name)[-1]  # e.g., .jpg
        unique_name = f"{uuid.uuid4()}{ext}"
        
        # Preserve upload_to folder
        if folder:
            file_path = f"{folder}/{unique_name}"
        else:
            file_path = unique_name
        
        content.seek(0)  # ✅ Make sure we're reading from the start
        
        self.client.storage.from_(self.bucket).upload(
            file_path,
            content.read(),
            file_options={"content-type": getattr(content, 'content_type', 'application/octet-stream')}
        )
        return file_path  # ✅ Return full path including folder
    
    def url(self, name):
        # ✅ Correct public URL format for Supabase
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{self.bucket}/{name}"
    
    def exists(self, name):
        try:
            folder = os.path.dirname(name)
            files = self.client.storage.from_(self.bucket).list(folder)
            filename = os.path.basename(name)
            return any(f['name'] == filename for f in files)
        except:
            return False
    
    def delete(self, name):
        self.client.storage.from_(self.bucket).remove([name])
    
    def size(self, name):
        return 0  # ✅ Required by Django Storage interface