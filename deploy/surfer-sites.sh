#!/usr/bin/env bash
# The websites that deploy to Cloudron Surfer, one line per site:
#   name  source folder in this repo  Surfer domain  token secret  folders/files left out
# "name" is what you say, e.g. "deploy identity website" -> identity.
# The CONTENTS of the source folder land at the Surfer root "/", never in a subfolder.
SITES='
spacerisk  spacerisk                  spacerisk.frivolddigital.com  SURFER_TOKEN_SPACERISK  content tools materials/*/sales
products   products-top-level-website products.frivolddigital.com   SURFER_TOKEN_PRODUCTS   content tools
identity   identity/website           identity.frivolddigital.com   SURFER_TOKEN_IDENTITY
cloud      cloud/website              cloud.frivolddigital.com      SURFER_TOKEN_CLOUD
historian  historian/website          historian.frivolddigital.com  SURFER_TOKEN_HISTORIAN
frontpage  frontpage                  frontpage.frivold.digital     SURFER_TOKEN_FRONTPAGE
'

# site_field <name> <column 1-4>  |  site_excludes <name>  |  site_names
site_line()     { printf '%s\n' "$SITES" | awk -v n="$1" '$1==n'; }
site_field()    { site_line "$1" | awk -v c="$2" '{print $c}'; }
site_excludes() { site_line "$1" | awk '{for (i=5;i<=NF;i++) print $i}'; }
site_names()    { printf '%s\n' "$SITES" | awk 'NF{print $1}'; }
