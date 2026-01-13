from types import MappingProxyType

EXTENSION_MAP = MappingProxyType(
    {
        # === Image ===
        "Image": {
            ".jpg", ".jpeg", ".png", ".gif", ".webp",
            ".svg", ".psd", ".raw"
        },
        # === Document ===
        "Document": {
            ".txt", ".md", ".pdf", ".docx", ".xlsx",
            ".pptx", ".log"
        },
        # === Audio ===
        "Audio": {
            ".mp3", ".wav", ".flac", ".aac", ".ogg",
            ".wma", ".m4a", ".opus", ".mid", ".ape",
        },
        # === Video ===
        "Video": {
            ".mp4", ".mkv", ".mov", ".avi", ".wmv",
            ".flv", ".webm", ".m4v", ".rmvb",
        },
        # === Code ===
        "Code": {
            ".c", ".cpp", ".py", ".java", ".js",
            ".ts", ".html", ".css", ".php", ".go",
            ".rs",
        },
        # === Data ===
        "Data": {
            ".json", ".yaml", ".yml", ".xml", ".sql",
            ".csv", ".nbt", ".dat", ".db", ".sqlite",
         },
        # === Archive ===
        "Archive": {
            ".zip", ".rar", ".7z", ".tar", ".gz",
            ".bz2", ".xz"
        },
        # === Executable ===
        "Executable": {
            ".exe", ".msi", ".bat", ".sh", ".ps1",
            ".dll", ".sys", ".iso", ".com", ".bin",
            ".deb", ".rpm", ".jar",
        },
        # === Specialized ===
        "Specialized": {
            ".litematic", ".schem", ".ttf", ".otf", ".cur"
        },
    }
)
