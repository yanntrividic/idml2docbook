This folder is for keeping track of how the book _Déborder Bolloré_ is getting converted to DocBook from HubXML.

```bash
python -m idml2docbook -tlg -o tests/bollo/bollo.dbk \
    -x tests/bollo/bollo.xml \
    --raster "jpg" --vector "svg" -f "images"
```

`post- coloniales` is to fix.