Hyou - Pythonic Interface to access Google Spreadsheet
======================================================

Hyou provides a simple Pythonic interface to access your
Google Spreadsheet data.

[![PyPI version](https://badge.fury.io/py/hyou.svg)](http://badge.fury.io/py/hyou)
[![Build Status](https://travis-ci.org/google/hyou.svg)](https://travis-ci.org/google/hyou)


Synopsis
--------

```python
import hyou

# Login to Google Spreadsheet with credentials
collection = hyou.login('/path/to/credentails.json')

# Open a spreadsheet by ID
spreadsheet = collection['1ZYeIFccacgHkL0TPfdgXiMfPCuEEWUtbhXvaB9HBDzQ']
print spreadsheet.title         # => "Hyou Test Sheet"

# Open a worksheet in a spreadsheet by sheet name
worksheet = spreadsheet['Sheet1']
print worksheet.title           # => "Sheet1"
print worksheet.rows            # => 5
print worksheet.cols            # => 3

# Worksheet objects can be accessed just like two-dimensional lists
print worksheet[1][0]           # => "banana"
print worksheet[1][1]           # => "50"

# Call Worksheet.commit() to apply changes
worksheet[2][0] = 'cinamon'
worksheet[2][1] = 40
worksheet.commit()
```

Documentation
-------------

Documentation is available at https://hyou.readthedocs.org/.


Author
------

Shuhei Takahashi

- Website: https://nya3.jp/
- Twitter: https://twitter.com/nya3jp/


Disclaimer
----------

This library is authored by a Googler and copyrighted by Google, but
is not an official Google product.


License
-------

Copyright 2015 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
