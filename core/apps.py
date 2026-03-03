import os
from pathlib import Path
from django.apps import AppConfig


def _compile_scss():
    """Compile static/scss/hellenvanmeene-website-custom.scss → static/css/…css."""
    try:
        import sass
        base = Path(__file__).resolve().parent.parent
        src = base / 'static' / 'scss' / 'hellenvanmeene-website-custom.scss'
        dst = base / 'static' / 'css' / 'hellenvanmeene-website-custom.css'
        dst.parent.mkdir(parents=True, exist_ok=True)
        css = sass.compile(filename=str(src), output_style='compressed')
        dst.write_text(css, encoding='utf-8')
    except Exception as exc:
        import warnings
        warnings.warn(f'SCSS compilation failed: {exc}')


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        _compile_scss()

        # Tell Django's dev-server autoreloader to watch the SCSS directory.
        # watch_dir with a glob is the reliable approach on Windows StatReloader.
        # When any .scss file changes the server restarts and _compile_scss() runs.
        try:
            from django.utils import autoreload

            def watch_scss(sender, **kwargs):
                base = Path(__file__).resolve().parent.parent
                scss_dir = base / 'static' / 'scss'
                sender.watch_dir(scss_dir, '*.scss')

            signal = getattr(autoreload, 'autoreload_started', None)
            if signal is not None:
                signal.connect(watch_scss)
        except Exception:
            pass  # not running under the dev server — safe to ignore
