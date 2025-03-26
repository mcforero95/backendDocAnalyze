from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Solo importa para que se registren los modelos, pero sin causar ciclos
import app.db.models.user  
import app.db.models.document  
import app.db.models.analysis  
import app.db.models.conversation
import app.db.models.document_chunk