"""Custom form widgets shared across admin forms."""

from django.forms.widgets import TextInput, Textarea
from django.utils.safestring import mark_safe


class EasyMDEWidget(Textarea):
    """
    Textarea that becomes a full EasyMDE Markdown editor in admin.
    Keyboard shortcuts: Ctrl+B bold, Ctrl+I italic, Ctrl+K code,
    Ctrl+L link, Ctrl+H heading, Ctrl+P preview.
    """

    def __init__(self, attrs=None):
        default_attrs = {"class": "easymde-widget"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        css = {"all": ("css/easymde.min.css",)}
        js = ("js/easymde.min.js", "js/easymde-init.js")


class BlobURLWidget(TextInput):
    """
    TextInput that auto-completes Azure Blob Storage filenames.

    Renders as a normal <input> with a <datalist> populated via a debounced
    fetch to the blob-autocomplete endpoint as the user types.
    No external JavaScript libraries required.

    Pass the full public container URL so no server-side env vars are needed::

        BlobURLWidget(
            container_url="https://hellenvanmeene.blob.core.windows.net/website-images"
        )
    """

    def __init__(self, attrs=None, container_url=""):
        super().__init__(attrs)
        self.container_url = container_url.rstrip("/")

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs or {})
        field_id = final_attrs.get("id", f"id_{name}")
        datalist_id = f"bloblist-{field_id}"
        final_attrs["list"] = datalist_id
        final_attrs["autocomplete"] = "off"

        input_html = super().render(name, value, final_attrs, renderer)

        script = f"""
<script>
(function () {{
  var input = document.getElementById('{field_id}');
  var datalist = document.getElementById('{datalist_id}');
  if (!input || !datalist) return;
  var timer;
  input.addEventListener('input', function () {{
    clearTimeout(timer);
    var q = input.value.split('/').pop();   // search on the filename part only
    if (q.length < 2) return;
    timer = setTimeout(function () {{
      var url = '/admin/blob-autocomplete/?container_url={self.container_url}&q=' + encodeURIComponent(q);
      fetch(url)
        .then(function (r) {{ return r.json(); }})
        .then(function (data) {{
          datalist.innerHTML = '';
          (data.results || []).forEach(function (blobUrl) {{
            var opt = document.createElement('option');
            opt.value = blobUrl;
            datalist.appendChild(opt);
          }});
        }})
        .catch(function () {{}});
    }}, 300);
  }});
}})();
</script>"""

        return mark_safe(
            f'<datalist id="{datalist_id}"></datalist>\n{input_html}\n{script}'
        )
