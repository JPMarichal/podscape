# app/social_media_formatters.py
import re
from bs4 import BeautifulSoup # For more robust HTML stripping

# Assuming interfaces.py is in the same package directory
from .interfaces import PostFormatter, PodcastItemDTO

class WhatsappFacebookFormatter(PostFormatter):
    """
    Formatea los episodios del podcast 'Mis lecturas sobre la fe' para publicaciones en WhatsApp y Facebook.
    """
    def format_post(self, item: PodcastItemDTO) -> str:
        """
        Genera un mensaje atractivo para redes sociales que promueve el episodio del podcast.
        Incluye título, descripción (limpia y recortada), y enlace para escuchar.
        """
        post_parts = []

        # Encabezado atractivo
        post_parts.append("✨ *MIS LECTURAS SOBRE LA FE* ✨\n")
        post_parts.append("📖 *Nuevo episodio disponible* 📖\n")

        # Título destacado
        post_parts.append(f"🎧 *{item.title.upper()}* 🎧\n")

        # Descripción (limpia y recortada)
        if item.description:
            soup = BeautifulSoup(item.description, "html.parser")
            desc_text = soup.get_text(separator=" ", strip=True)
            
            # Acortar descripción si es muy larga
            max_desc_length = 280  # Longitud máxima para la descripción
            if len(desc_text) > max_desc_length:
                desc_text = desc_text[:max_desc_length].rsplit('. ', 1)[0] + '...'
            
            if desc_text:
                post_parts.append(f"🔍 *Sobre este estudio:*\n{desc_text}\n")

        # Llamado a la acción
        post_parts.append("\n🎧 *¡No te pierdas este interesante análisis!* 🎧\n")
        
        # Usamos directamente item.link que es el enlace al episodio (GUID)
        post_parts.append(f"🔗 Escucha el episodio completo aquí:\n{item.link}\n")

        # Hashtags relevantes
        post_parts.append("\n#EstudiosBíblicos #FeSUD #SantosDeLosÚltimosDías #Escrituras #Jesucristo #Restauración #VerdadEterna #DoctrinaCristiana #EstudiosBíblicosSUD")

        return "\n".join(post_parts)

class PlainTextFormatter(PostFormatter):
    """
    A simpler formatter that outputs plain text, useful for debugging or other contexts.
    """
    def format_post(self, item: PodcastItemDTO) -> str:
        """Generates a simple plain text representation of the podcast item."""
        description_snippet = (item.description[:75] + "...") if item.description and len(item.description) > 75 else (item.description or "N/A")
        
        # Clean description snippet
        soup = BeautifulSoup(description_snippet, "html.parser")
        cleaned_description_snippet = soup.get_text(separator=" ", strip=True)

        return (
            f"Título: {item.title}\n"
            f"Enlace: {item.link}\n"
            f"Audio: {item.audio_url or 'N/A'}\n"
            f"Imagen: {item.image_url or 'N/A'}\n"
            f"Descripción: {cleaned_description_snippet}\n"
            f"Publicado: {item.published_date or 'N/A'}"
        )
