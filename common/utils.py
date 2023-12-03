import magic


def get_mime_type(obj):
    """
    Get MIME by reading the header of the file
    """
    file = obj.file
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    return mime_type
