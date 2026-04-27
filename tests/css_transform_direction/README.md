This folder is to test out whether the file is correctly normalised despite weird InDesign direct formatting.

```sh
python -m idml2docbook \
    -x tests/css_transform_direction/css_transform_direction.xml \
    -t --ignore-overrides \
    -o tests/css_transform_direction/css_transform_direction.dbk
```