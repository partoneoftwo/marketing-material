# Cloud

Marketing material for Many Worlds Cloud, laid out the same way as [`historian/`](../historian). Many Worlds Cloud is a
front end to the open-source cloud security scanner Prowler: it shows the same kind of report as Many Worlds Historian
and sends risks, incidents and tasks to SpaceRisk.

- **Website:** `website/`, in English, Norwegian (bokmål) and Spanish. Same look as the Historian site. The folder is
  self-contained and can be uploaded to any static host on its own. No cookies, no third-party requests, and no scripts
  apart from the language redirect.
- **Texts** in `content/<lang>.json` (nb and es were machine-written from English; have a native speaker review them).
  Check with `python cloud/tools/check_content.py`. Rebuild with `python cloud/tools/build_site.py` (needs `jinja2`).
  Adding a language is one more content file: de, fr, it and pt-br are picked up when they exist.
- **Report tables** on the pages are illustrations with invented data, and say so, because the product is in
  development. Replace them with real screens (as on the Historian site) when the product has them.
